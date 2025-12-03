import os
import asyncio
import multiprocessing as mp
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect
import uvicorn

# Import managers
from db_manager import DatabaseManager
from state_manager import StateManager
from connection_manager import ConnectionManager

# Import routers
from routers import presets, gradients, system, controller

class UDPBroadcastProtocol(asyncio.DatagramProtocol):
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    def datagram_received(self, data, addr):
        if data == b'trigger_cube_update':
            asyncio.create_task(self.connection_manager.broadcast_cube_data())
        else:
            asyncio.create_task(self.connection_manager.broadcast_udp(data))

class WebSocketAPIServer:
    def __init__(self, state):
        # Define lifespan context manager
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            loop = asyncio.get_running_loop()
            transport = None
            try:
                transport, protocol = await loop.create_datagram_endpoint(
                    lambda: UDPBroadcastProtocol(self.connection_manager),
                    local_addr=('127.0.0.1', 8001)
                )
                self.udp_transport = transport
                print("UDP Bridge listening on 127.0.0.1:8001")
            except Exception as e:
                print(f"Failed to start UDP server: {e}")

            # --- STARTUP LOGIC ABOVE ---
            yield # Application runs here
            # --- SHUTDOWN LOGIC BELOW ---

            print("Shutting down UDP Bridge...")
            if self.udp_transport:
                self.udp_transport.close()
                await asyncio.sleep(0.5)  # Wait for cleanup
                print("UDP Bridge closed")
            print("Server shutdown complete")

        # Pass lifespan to FastAPI
        self.app = FastAPI(lifespan=lifespan)

        # 1. Initialize Managers & State
        self.db = DatabaseManager()
        self.state_manager = StateManager(state)
        self.cube_state = state

        # 2. Setup Shared Memory
        self.shared_mem = mp.shared_memory.SharedMemory(name="cube_data")
        self.array = np.ndarray(
            shape=(9, 1000, 3),
            dtype=np.float32,
            buffer=self.shared_mem.buf
        )

        # 3. Initialize Connection Manager
        self.connection_manager = ConnectionManager(self.cube_state, self.array)

        # 4. Store in app.state for Routers
        self.app.state.connection_manager = self.connection_manager
        self.app.state.db = self.db
        self.app.state.state_manager = self.state_manager
        self.app.state.cube_state = self.cube_state

        # UDP transport placeholder
        self.udp_transport = None

        # 5. Middleware
        self.app.add_middleware(
            CORSMiddleware, allow_origins=["*"], allow_credentials=True,
            allow_methods=["*"], allow_headers=["*"]
        )

        # 6. Mount the mobile app static files
        self.dist_path = os.path.join(os.path.dirname(__file__), "../mobile/dist")
        if os.path.exists(self.dist_path):
            self.app.mount("/assets", StaticFiles(directory=f"{self.dist_path}/assets"), name="assets")

        # 7. Mount Routers
        self.app.include_router(presets.router)
        self.app.include_router(controller.router)
        self.app.include_router(gradients.router)
        self.app.include_router(system.router)

        # 8. Initialize Core Routes
        self.init_core_routes()

    def init_core_routes(self):
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket, skip: int = Query(1)):
            try:
                await self.connection_manager.connect(websocket, skip)
                while True:
                    try:
                        await websocket.receive_json()
                    except WebSocketDisconnect:
                        break
            finally:
                self.connection_manager.disconnect(websocket)

    def run(self, host="0.0.0.0", port=8000):
        print(f'Server starting on {host}:{port}...')
        uvicorn.run(self.app, host=host, port=port, access_log=False, log_level="warning")
