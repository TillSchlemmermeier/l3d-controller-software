from fastapi import FastAPI, WebSocket, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import sqlite3
import json
from typing import List, Optional
from copy import deepcopy
from UltraDict import UltraDict
from typing import List
import multiprocessing as mp
import numpy as np
from starlette.websockets import WebSocketDisconnect
from pathlib import Path
from db_manager import DatabaseManager
from state_manager import StateManager


class WebSocketAPIServer:
    def __init__(self):
        self.app = FastAPI()
        self.db = DatabaseManager()
        self.state_manager = StateManager()
        self.init_routes()
        self.state = UltraDict(name='state')
        self.active_websockets: List[WebSocket] = []
        self.shared_mem = mp.shared_memory.SharedMemory(name="cube_data")
        self.array = np.ndarray(
            shape=(9, 1000, 3),
            dtype=np.float32, 
            buffer=self.shared_mem.buf
        )

        # Enable CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )

    def init_routes(self):
        @self.app.get("/")
        async def root():
          return {"message": "Hello World"}

        # frontend request to get the current state through the websocket
        @self.app.get("/api/get-state")
        async def get_present_state():
            await update_state()

        # get a list with all the available generators or effects
        @self.app.get('/api/get-element-names/{type}')
        async def get_names(type):
            element_names = self.db.get_element_names(type)
            return JSONResponse(content=element_names)

        # get a list with all the active generators or effects
        @self.app.get('/api/get-active-elements/{type}')
        async def get_active_elements(type):
            active_elements = self.db.get_active_elements(type)
            return JSONResponse(content=active_elements)

        # get all the information available in the database for a generator or effect
        @self.app.get('/api/get-element-info/{type}/{element_name}')
        async def get_element_info(type, element_name):
            element = self.db.get_element_info(type, element_name)
            return JSONResponse(content=element)

        # get a list with all the preset names for a given generator or effect
        @self.app.get('/api/get-presets/{type}/{element_name}')
        async def get_presets(type, element_name):
            presets = self.db.get_preset_names(type, element_name)
            return JSONResponse(content=presets)

        # get all the information available in the database for a given preset
        @self.app.get('/api/get-preset-info/{type}/{element}/{preset}')
        async def get_element_info(type, element, preset):
            preset = self.db.get_preset_info(type, element, preset)
            return JSONResponse(content=preset)

        # rename a given preset in the db and in the filesystem
        @self.app.get('/api/rename-preset/{type}/{element}/{old_preset}/{new_preset}')
        async def rename_preset(type, element, old_preset, new_preset):
            success = self.db.rename_preset(type, element, old_preset, new_preset)
            if not success:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Failed to rename preset"}
                )
            # rename the gif if present
            PREVIEW_DIR = Path("../src/assets/previews")
            PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

            old_file_path = PREVIEW_DIR / f"{element}_p_{old_preset}.gif"
            new_file_path = PREVIEW_DIR / f"{element}_p_{new_preset}.gif"
            print(f"Renaming {old_file_path} to {new_file_path}")
            if old_file_path.exists():
                print("File Path exists")
                old_file_path.rename(new_file_path)
                return JSONResponse(
                    status_code=200,
                    content={"message": "Preset renamed successfully"}
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Failed to rename preset"}
                )

        # delete preset
        @self.app.get('/api/delete-preset/{type}/{element}/{preset}')
        async def delete_preset(type, element, preset):
            success = self.db.delete_preset(type, element, preset)
            if success:
                return JSONResponse(
                    status_code=200,
                    content={"message": "Preset deleted successfully"}
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Failed to delete preset"}
                )

        # delete element
        @self.app.get('/api/delete-element/{type}/{element}')
        async def delete_element(type, element):
            success = self.db.delete_element(type, element)
            if success:
                return JSONResponse(
                    status_code=200,
                    content={"message": "Element deleted successfully"}
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Failed to delete element"}
                )

        # add new element
        @self.app.get('/api/add-element/{type}/{element}')
        async def add_element(type, element):
            success = self.db.add_element(type, element)
            if success:
                return JSONResponse(
                    status_code=200,
                    content={"message": "Element added successfully"}
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Failed to add element"}
                )
                
        # toggle the active state of a generator or effect
        @self.app.get('/api/toggle-element-active/{type}/{element}')
        async def toggle_element_active(type, element):
            success = self.db.toggle_element_active(type, element)
            if success:
                return JSONResponse(
                    status_code=200,
                    content={"message": "Toggled element active successfully"}
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Failed to toggle element active"}
                )

        # validate all presets
        @self.app.get('/api/validate-presets')
        async def validate_presets():
            try:
                from preset_validator import PresetValidator
                
                validator = PresetValidator()
                validation_results = validator.validate_all()
                
                return JSONResponse(
                    status_code=200,
                    content=validation_results
                )
                
            except Exception as e:
                print(f"Error validating presets: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"message": f"Error validating presets: {str(e)}"}
                )

        # load a given preset in the state    
        @self.app.get('/api/load/{type}/{preset}/{channel}/{effectIndex}/{element}')
        async def load(type: str, preset: str, channel: int, effectIndex: int, element: str):
            preset_data = self.db.get_preset(type, element, preset)
            if type == 'generator':
                if channel not in self.state:
                    this_channel = self.db.get_preset('channel', 'presets', 'blank')
                    self.state_manager.load_generator(channel, preset_data, this_channel)
                else:
                    self.state_manager.load_generator(channel, preset_data)
            elif type == 'effect':
                self.state_manager.load_effect(channel, effectIndex, preset_data)
            elif type == 'channel':
                self.state_manager.load_channel(channel, preset_data)
            elif type == 'global':
                self.state_manager.load_global(preset_data)

            await update_state()
            return {'message': f'{type} loaded successfully'}

        # save a new preset in the database       
        @self.app.post('/api/save/')
        async def save(
            preset: str = Form(...),
            type: str = Form(...),
            channel: int = Form(...),
            index: int = Form(...),
            preview: UploadFile = File(None),
            force: bool = Form(False)
        ):
            success = False
            message = ""

            # Determine the correct element name based on type
            element = 'presets'  # default for channel and global
            if type == 'generator':
                element = self.state[channel][9]['name']
            elif type == 'effect':
                element = self.state[channel][index]['name']

            if not force and self.db.preset_exists(type, element, preset):
                return JSONResponse(
                    status_code=409,  # Conflict
                    content={"message": f"Preset '{preset}' already exists"}
                )

            if type == 'channel':
                data = dict(self.state[channel])
                filename = f'channel_p_{preset}'
            elif type == 'global':
                data = dict(self.state)
                filename = f'global_p_{preset}'
            elif type == 'generator':
                print('saving generator')
                data = dict(self.state[channel][9])
                filename = f'{element}_p_{preset}'
                print(success)
            elif type == 'effect':
                data = dict(self.state[channel][index])
                filename = f'{element}_p_{preset}'
    
            success, message = self.db.save_preset(type, element, preset, data)

            if not success:
                return JSONResponse(
                    status_code=400,
                    content={"message": message}
                )

            PREVIEW_DIR = Path("../src/assets/previews")
            PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
            
            if preview:
                # Save the GIF file
                file_path = PREVIEW_DIR / f"{filename}.gif"
                with open(file_path, "wb") as buffer:
                    content = await preview.read()
                    buffer.write(content)

            return JSONResponse(
                status_code=200,
                content={"message": "Preset saved successfully"}
            )

        # remove an effect or a channel
        @self.app.get('/api/remove/{type}/{channelIndex}/{effectIndex}')
        async def remove(type: str, channelIndex: int, effectIndex: int):
            if type == 'channel':
                if self.state['numberOfChannels'] == 1:
                    return {'message': 'Cannot delete the only channel'}
                self.state_manager.remove_channel(channelIndex)
            if type == 'effect':
                self.state_manager.remove_effect(channelIndex, effectIndex)
            await update_state()
            return {'message': type +  ' deleted'}

        # copy a channel
        @self.app.get('/api/copychannel/{channel}')
        async def copychannel(channel: int):
            self.state_manager.copy_channel(channel)
            await update_state()
            return {'message': 'Channel copied'}
        
        # move a channel
        @self.app.get('/api/movechannel/{from_index}/{to_index}')
        async def movechannel(from_index: int, to_index: int):
            self.state_manager.move_channel(from_index, to_index)
            await update_state()
            return {'message': 'Channel moved'}
        
        # move an effect
        @self.app.get('/api/moveeffect/{channelIndex}/{fromIndex}/{toIndex}')
        async def moveeffect(channelIndex:int, fromIndex: int, toIndex: int):
            self.state_manager.move_effect(channelIndex, fromIndex, toIndex)
            await update_state()
            return {'message': 'Effect moved'}

        # copy an effect
        @self.app.get('/api/copyeffect/{from_channel}/{from_effectIndex}/{to_channel}/{to_effectIndex}')
        async def copyeffect(from_channel: int, from_effectIndex: int, to_channel: int, to_effectIndex: int):
            self.state_manager.copy_effect(from_channel, from_effectIndex, to_channel, to_effectIndex)
            await update_state()
            return {'message': 'Effect copied'}
        
        # toggle an effect
        @self.app.get('/api/toggleeffect/{channelIndex}/{effectIndex}')
        async def toggleeffect(channelIndex: int, effectIndex: int):
            self.state_manager.toggle_effect(channelIndex, effectIndex)
            await update_element(channelIndex, effectIndex)
            return {'message': 'Effect toggled'}
        
        # select a new context for the midi-controller
        @self.app.get('/api/select/{channelIndex}/{elementIndex}')
        async def select(channelIndex: int, elementIndex: int):
            self.state['context'] = [channelIndex, elementIndex]
            self.state['midi_update'] = 1
            await update_state()
            return {"message": "Selected"}

        # toggle autopilot
        @self.app.get('/api/toggle-autopilot')
        async def toggle_autopilot():
            self.state_manager.toggle_autopilot()
            await update_state()
            return {"message": "Autopilot toggled"}

        # change autopilot mode
        @self.app.get('/api/autopilot-mode')
        async def autopilot_mode():
            self.state_manager.autopilot_mode()
            await update_state()
            return {"message": "Autopilot mode changed"}

        # create a websocket connection
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            try:
                await websocket.accept()
                self.active_websockets.append(websocket)
                print('websocket connected')

                # Send initial message
                await websocket.send_json({
                    "type": "state_update",
                    "data": {"status": "connected"}
                })

                # Keep websocket connection alive
                while True:
                    try:
                         # listen for incoming messages
                        data = await websocket.receive_json()
                    except WebSocketDisconnect:
                        break
            except Exception as e:
                print(f"WebSocket error: {e}")
            finally:
                # Clean up connection
                if websocket in self.active_websockets:
                    self.active_websockets.remove(websocket)
                    print('WebSocket disconnected')

        # update the value of a single key in the frontend
        @self.app.get("/api/update_key/{key}")
        async def update_key(key: str, channel: Optional[int] = None):
            if channel is None:
                value = self.state[key]
            else:
                value = self.state[channel][key]

            message = {
                "type": "state_key",
                "data": { 'key': key, 'value': value, 'channel': channel }
            }
            return await stream_data(message)

        # update the value of a single element in the frontend
        @self.app.get('/api/update_element/{channel}/{element}')
        async def update_element(channel: int, element: int):
            message = {
                "type": "state_section",
                "data": { channel: { element: self.state[channel][element] }}
            }
            return await stream_data(message)

        # update the whole state in the frontend
        @self.app.get('/api/update_state')
        async def update_state():
            message = {
                "type": "state",
                "data": dict(self.state)
            }
            return await stream_data(message)

        # send the cube data to the frontend
        @self.app.get('/api/update_cube')
        async def update_cube():
            # Only send combined view (index 0) and active channels
            with self.state.lock:
                num_channels = self.state['numberOfChannels']
            message = {
                "type": "cube_data",
                "data": self.array[0:num_channels + 1].copy().tolist()
            }
            return await stream_data(message)
          
        # send data to frontend through websocket
        @self.app.post("/api/stream")
        async def stream_data(message: dict):
            # message types can be: cube_data, state, state_section, state_key, spectrum_data
            for websocket in self.active_websockets:
                await websocket.send_json(message)

            return {"message": "Data streamed successfully"}

    
    def run(self, host="0.0.0.0", port=8000):
        print('running server')
        # uvicorn.run(self.app, host=host, port=port)
        # No logging in console
        uvicorn.run(self.app, host=host, port=port, access_log=False)
