from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import sqlite3
import json
from typing import List
from copy import deepcopy
from UltraDict import UltraDict
from pydantic import BaseModel
from typing import List
from enum import Enum
import multiprocessing as mp
import numpy as np

class MessageType(Enum):
    CUBE_DATA = "cube_data"
    SPECTRUM_DATA = "spectrum_data"
    MIDI_UPDATE = "midi_update"
    STATE_UPDATE = "state_update"
    ERROR = "error"


class CubeDataModel(BaseModel):
     # Shape: (9, 1000, 4) - Combined cube + 8 channels, LEDs, RGBA
    colors: List[List[List[float]]] 

class CubeDataSharedMemory:
    def __init__(self):
        self.shape = (9, 1000, 4)  # 9 channels, 1000 LEDs, RGBA
        self.size = np.prod(self.shape) * 4  # 4 bytes per float32
        try:
            self.shm = mp.shared_memory.SharedMemory(name="cube_data", create=True, size=self.size)
        except FileExistsError:
            self.shm = mp.shared_memory.SharedMemory(name="cube_data")
        
        self.array = np.ndarray(self.shape, dtype=np.float32, buffer=self.shm.buf)    

class class_gui_server:
    def __init__(self, state):
        self.app = FastAPI()
        self.init_routes()
        self.init_db()
        self.state = UltraDict(name='state')
        self.active_websockets: List[WebSocket] = []
        self.shared_mem = CubeDataSharedMemory()

        # Enable CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )

    def init_db(self):
        print('init db')
        # conn = sqlite3.connect('l3ddb.db')
        # cursor = conn.cursor()
        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS channel_presets (
        #         id INTEGER PRIMARY KEY,
        #         name TEXT,
        #         data TEXT
        #     )
        # ''')
        # conn.commit()
        # conn.close()
      
    # async def connect(self, websocket: WebSocket):
    #     """connect event"""
    #     await websocket.accept()
    #     self.active_websockets.append(websocket)
    
    def update_channel(self, channelKey):
        channel = self.state[channelKey]
        channel['update'] = 1
        if channelKey != 9:
            channel['generator']['update'] = 1
        for i in range(len(channel['effects'])):
            channel['effects'][i]['update'] = 1
        self.state[channelKey] = channel


    def init_routes(self):
        @self.app.get("/")
        async def root():
          return {"message": "Hello World"}

        @self.app.get("/api/get-state")
        async def get_present_state():
            await stream_data({'type': 'state'})
            # print('get state')
            # print(self.state)
            # return self.state
        

        # fetch a list of names of all basic generators and effects or all channel and global presets
        @self.app.get('/api/get-names/{type}')
        async def get_names(type):
            conn = sqlite3.connect('l3d.db')
            cursor = conn.cursor()
            if type == 'generator':
                cursor.execute('SELECT generator FROM generators WHERE name = "basic"'),
            elif type == 'effect':
                cursor.execute('SELECT effect FROM effects WHERE name = "basic"'),
            elif type == 'channel':
                cursor.execute('SELECT name FROM presets WHERE type = "channel"'),
            elif type == 'global':
                cursor.execute('SELECT name FROM presets WHERE type = "global"'),
                return JSONResponse(content={'message': 'Invalid type'}, status_code=400)

            rows = cursor.fetchall()
            conn.close()
            names = [row[0] for row in rows]
            if rows:
                return JSONResponse(content=names)
            else:
                return JSONResponse(content={'message': f'{type.capitalize()} not found'}, status_code=404)
    
        # get a list with all the preset names for a given generator or effect
        @self.app.get('/api/get-presets/{type}/{name}')
        async def get_presets(type, name):
            conn = sqlite3.connect('l3d.db')
            cursor = conn.cursor()
            if type == 'generator':
                cursor.execute('SELECT name FROM generators WHERE generator = ?', (name,)),
            elif type == 'effect':
                cursor.execute('SELECT name FROM effects WHERE effect = ?', (name,)),
            else:
                return JSONResponse(content={'message': 'Invalid type'}, status_code=400)

            rows = cursor.fetchall()
            conn.close()
            names = [row[0] for row in rows]
            if rows:
                return JSONResponse(content=names)
            else:
                return JSONResponse(content={'message': f'{type.capitalize()} not found'}, status_code=404)
            
        # load a generator or effect into a channel
        @self.app.get('/api/load/{type}/{preset}/{channel}/{effectIndex}/{name}')
        async def load(type, preset, channel: int, effectIndex: int, name):
            this_channel = self.state[channel]
            if channel == self.state['numberOfChannels']:
                self.state['numberOfChannels'] += 1
            if type == 'generator':
                if preset == 'basic':
                    generator = this_channel['generator']
                    generator['name'] = name
                    generator['IO'] = 1
                    generator['update'] = 1
                    generator['params'] = []
                    this_channel['update'] = 1
                else:
                    conn = sqlite3.connect('l3d.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT data FROM generators WHERE generator = ? AND name = ?"', (name, preset))
                    row = cursor.fetchone()
                    conn.close()
                    if row:
                        generator_data = json.loads(row[0])
                        generator_data['update'] = 1
                        this_channel['update'] = 1
                        this_channel['generator'] = generator_data
                    else:
                        return JSONResponse(content={'message': 'Generator not found'}, status_code=404)
                    
                self.state[channel] = this_channel

            elif type == 'effect': 
                if preset == 'basic':
                    effect = {
                        'IO': 1,
                        'name': name,
                        'update': 1,
                        'params': [],
                    }
                    if effectIndex < len(this_channel['effects']):
                        this_channel['effects'][effectIndex] = effect
                    else:
                        this_channel['effects'].append(effect)
                    this_channel['update'] = 1
                else:
                    conn = sqlite3.connect('l3d.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT data FROM effects WHERE effect = ? AND name = ?', (name, preset))
                    row = cursor.fetchone()
                    conn.close()
                    if row:
                        effect_data = json.loads(row[0])
                        effect_data['update'] = 1
                        this_channel['update'] = 1
                        this_channel[effectIndex] = effect_data
                    else:
                        return JSONResponse(content={'message': 'Effect not found'}, status_code=404)
                    
                self.state[channel] = this_channel
                print('from server', self.state[channel])

            elif type == 'channel':
                conn = sqlite3.connect('l3d.db')
                cursor = conn.cursor()
                cursor.execute('SELECT data FROM presets WHERE type = "channel" AND name = ?', (name,))
                row = cursor.fetchone()
                conn.close()
                if row:
                    channel_data = json.loads(row[0])
                    this_channel.clear()
                    this_channel = {key: value for key, value in channel_data.items()}
                    self.update_channel(channel)
                else:
                    return JSONResponse(content={'message': 'Channel not found'}, status_code=404)
                
                self.state[channel] = this_channel
                
            elif type == 'global':
                conn = sqlite3.connect('l3d.db')
                cursor = conn.cursor()
                cursor.execute('SELECT data FROM presets WHERE type = "global" AND name = ?', (name,))
                row = cursor.fetchone()
                conn.close()
                if row:
                    global_data = json.loads(row[0])
                    self.state = {key: value for key, value in global_data.items()}
                    for i in range(global_data['numberOfChannels']):
                        self.update_channel(i)
                else:
                    return JSONResponse(content={'message': 'Global preset not found'}, status_code=404)
            return {'message': type + ' loaded'}
            

        # delete an effect or a channel
        @self.app.get('/api/remove/{type}/{channelIndex}/{effectIndex}')
        async def remove(type: str, channelIndex: int, effectIndex: int):
            if type == 'channel':
                self.state['numberOfChannels'] -= 1
                for i in range(channelIndex, self.state['numberOfChannels']):
                    this_channel = self.state[i]
                    this_channel.clear()
                    for key, value in self.state[i + 1].items():
                        this_channel[key] = value
                    self.update_channel(i)
                    
                del self.state[self.state['numberOfChannels']]

            if type == 'effect':
                this_channel = self.state[channelIndex]
                del this_channel['effects'][effectIndex]
                self.state[channelIndex] = this_channel
                self.update_channel(channelIndex)

            return {'message: ' + type + ' deleted'}


        # copy a channel
        @self.app.get('/api/copychannel/{channel}')
        async def copychannel(channel: int):
            newChannelKey = self.state['numberOfChannels']
            newChannel = deepcopy(self.state[channel])
            self.state[newChannelKey] = newChannel
            self.update_channel(newChannelKey)
            self.state['numberOfChannels'] += 1

            return {'message': 'Channel copied'}
        
        # move a channel
        @self.app.get('/api/movechannel/{from_index}/{to_index}')
        async def movechannel(from_index: int, to_index: int):
            temp_channel = {}
            for key, value in self.state[from_index].items():
                temp_channel[key] = value

            if from_index < to_index:
                for i in range(from_index, to_index):
                    self.state[i].clear()
                    for key, value in self.state[i + 1].items():
                        self.state[i][key] = value

            elif from_index > to_index:
                for i in range(to_index, from_index):
                    self.state[i + 1].clear()
                    for key, value in self.state[i].items():
                        self.state[i + 1][key] = value

            self.state[to_index].clear()
            self.state[to_index] = {key: value for key, value in temp_channel.items()}

            for i in range (min(from_index, to_index), max(from_index, to_index) + 1):
                self.update_channel(i)
            return {'message': 'Channel moved'}
        
        # move an effect
        @self.app.get('/api/moveeffect/{channelIndex}/{fromIndex}/{toIndex}')
        async def moveeffect(channelIndex:int, fromIndex: int, toIndex: int):
            channel = self.state[channelIndex]
            effect = deepcopy( channel['effects'][fromIndex])
            del channel['effects'][fromIndex]
            channel['effects'].insert(toIndex, effect)
            for i in range(min(fromIndex, toIndex), max(fromIndex, toIndex) + 1):
                channel['effects'][i]['update'] = 1
            channel['update'] = 1
            self.state[channelIndex] = channel

            return {'message': 'Effect moved'}


        # copy an effect
        @self.app.get('/api/copyeffect/{from_channel}/{from_effectIndex}/{to_channel}/{to_effectIndex}')
        async def copyeffect(from_channel: int, from_effectIndex: int, to_channel: int, to_effectIndex: int):
            effect = deepcopy(self.state[from_channel]['effects'][from_effectIndex])
            this_channel = self.state[to_channel]
            this_channel['effects'].insert(to_effectIndex, effect)
            self.state[to_channel] = this_channel
            self.update_channel(to_channel)

            return {'message': 'Effect copied'}
        

        # save Presets
        @self.app.get('/api/save/{type}/{name}/{channel}/{index}')
        async def save(type, name, channel, index):
            index = int(index)
            conn = sqlite3.connect('l3d.db')
            cursor = conn.cursor()
            if type == 'channel':
                channel_data = dict(self.state[channel])
                cursor.execute('''
                    INSERT INTO presets (type, name, data) VALUES (?, ?, ?)
                ''', ('channel', name, json.dumps(channel_data)))
            elif type == 'global':
                global_data = dict(self.state)
                cursor.execute('''
                    INSERT INTO presets (type, name, data) VALUES (?, ?, ?)
                ''', ('global', name, json.dumps(global_data)))
            elif type == 'generator':
                generator_data = dict(self.state[channel]['generator'])
                cursor.execute('''
                    INSERT INTO generators (generator, name, data) VALUES (?, ?, ?)
                ''', (generator_data['name'], name, json.dumps(generator_data)))
            elif type == 'effect':
                effect_data = dict(self.state[channel]['effects'][index])
                cursor.execute('''
                    INSERT INTO effects (effect, name, data) VALUES (?, ?, ?)
                ''', (effect_data['name'], name, json.dumps(effect_data)))
            conn.commit()
            conn.close()
            return {"message": "Preset saved successfully"}
        
        # delete presets
        @self.app.get('/api/delete/{type}/{preset}/{name}')
        async def delete(type, preset, name):
            conn = sqlite3.connect('l3d.db')
            cursor = conn.cursor()
            if type == 'channel':
                cursor.execute('''
                    DELETE FROM presets WHERE type = "channel" AND name = ?
                ''', (preset,))
            elif type == 'global':
                cursor.execute('''
                    DELETE FROM presets WHERE type = "global" AND name = ?
                ''', (preset,))
            elif type == 'generator':
                cursor.execute('''
                    DELETE FROM generators WHERE generator = ? AND name = ?
                ''', (name, preset,))
            elif type == 'effect':
                cursor.execute('''
                    DELETE FROM effects WHERE effect = ? AND name = ?
                ''', (name, preset))
            conn.commit()
            conn.close()
            return {"message": "Preset deleted successfully"}
        
        # select parameter editor
        @self.app.get('/api/select/{coords}')
        async def select(coords):
            coords = coords.split(',')
            x = int(coords[0])
            y = int(coords[1])
            self.state['context'] = [x, y]
            print(self.state['context'])
            return {"message": "Selected"}


        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.active_websockets.append(websocket)
            print('websocket connected')

            # Send initial message
            await websocket.send_json({
                "type": "state_update",
                "data": {"status": "connected"}
            })

            while True:
                data = await websocket.receive_json()
                if data.get('type') == 'midi':
                    # Handle MIDI updates
                    self.state['midi_update'] = 1
                    midi_values = self.state['midi_values']
                    midi_values[int(data['index'])] = float(data['value'])
                    self.state['midi_values'] = midi_values
                    
                    # Send acknowledgment
                    await websocket.send_json({
                        "type": "midi_update",
                        "data": {"status": "success"}
                    })

    
        # send data to frontend through websocket
        @self.app.post("/api/stream")
        async def stream_data(message: dict):
            if message['type'] == 'cube_data':
                message['data'] = self.shared_mem.array.copy().tolist()
            if message['type'] == 'state':
                message['data'] = dict(self.state)
            # message = {
            #     "type": data['type'],
            #     "data": data['data']
            # }
            for websocket in self.active_websockets:
                await websocket.send_json(message)
            return {"message": "Data streamed successfully"}


    
    def run(self, host="0.0.0.0", port=8000):
        print('running server')
        # uvicorn.run(self.app, host=host, port=port)
        # No logging in console
        uvicorn.run(self.app, host=host, port=port, access_log=False)


if __name__ == "__main__":
    server = class_gui_server()
    server.run()