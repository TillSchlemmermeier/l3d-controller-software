import asyncio
from typing import List, Optional
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self, state, array):
        self.active_websockets: List[WebSocket] = []
        self.websocket_settings = {}
        self.state = state
        self.array = array
        # set by the UDP trigger, awaited by the single broadcast consumer below
        self.frame_ready = asyncio.Event()


    async def connect(self, websocket: WebSocket, skip: int):
        await websocket.accept()
        self.active_websockets.append(websocket)
        self.websocket_settings[websocket] = {
            'skip': skip,
            'count': 0
        }
        print(f"WebSocket connected. Skip: {skip}. Total: {len(self.active_websockets)}")
        # Send initial status
        await websocket.send_json({"type": "state_update", "data": {"status": "connected"}})


    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_websockets:
            self.active_websockets.remove(websocket)
        if websocket in self.websocket_settings:
            del self.websocket_settings[websocket]
        print("WebSocket disconnected")


    # send a JSON message to all connected clients
    async def stream_data(self, message: dict):
        for websocket in list(self.active_websockets):
            try:
                await websocket.send_json(message)
            except Exception:
                self.disconnect(websocket)


    # Forwards raw UDP text to websockets, used for s2l data
    async def broadcast_udp(self, data: bytes):
        text = data.decode('utf-8')
        for websocket in list(self.active_websockets):
            # Only send if skip is 1 (no throttling) i.e. electron frontend
            if self.websocket_settings.get(websocket, {}).get('skip', 1) == 1:
                await websocket.send_text(text)


    # Flag that a new cube frame is ready. Setting an Event coalesces bursts, so frames
    # that arrive while a send is in flight are dropped — we only ever send the latest one.
    def notify_frame_ready(self):
        self.frame_ready.set()

    # wait for a frame, send the LATEST one to all clients, repeat.
    async def run_broadcast_consumer(self):
        while True:
            await self.frame_ready.wait()
            self.frame_ready.clear()
            try:
                await self._send_latest_frame()
            except Exception as e:
                # never let a send error kill the consumer
                print(f"[broadcast] error sending cube frame: {e}")

    async def _send_latest_frame(self):
        if not self.active_websockets:
            return
        # Access state without lock for speed
        num_channels = self.state['numberOfChannels']
        binary_data = self.array[0:num_channels + 1].tobytes()

        for ws in list(self.active_websockets):
            settings = self.websocket_settings.get(ws)
            if settings:
                settings['count'] += 1
                if settings['count'] % settings['skip'] != 0:
                    continue
            try:
                await ws.send_bytes(binary_data)
            except Exception:
                # drop a dead/slow client instead of crashing the consumer
                self.disconnect(ws)


    # send the cube data to the frontend as JSON (legacy function)
    async def update_cube(self):
        # Only send combined view (index 0) and active channels
        with self.state.lock:
            num_channels = self.state['numberOfChannels']
        message = {
            "type": "cube_data",
            "data": self.array[0:num_channels + 1].copy().tolist()
        }
        return await self.stream_data(message)
    

    # update the full state in the frontend
    async def update_state(self):
        with self.state.lock:
            message = {
                "type": "state",
                "data": dict(self.state)
            }
        await self.stream_data(message)


    # update the value of a single element in the frontend
    async def update_element(self, channel: int, element: int):
        with self.state.lock:
            # Handle case where element might be None (e.g. channel key update)
            if element is not None:
                data = { channel: { element: self.state[channel][element] }}
            else:
                data = { channel: dict(self.state[channel]) }
                
            message = {
                "type": "state_section",
                "data": data
            }
        await self.stream_data(message)


    # update the value of a single key in the frontend
    async def update_key(self, key: str, channel: Optional[int] = None):
        if channel is None:
            value = self.state[key]
        else:
            value = self.state[channel][key]

        message = {
            "type": "state_key",
            "data": { 'key': key, 'value': value, 'channel': channel }
        }
        return await self.stream_data(message)
