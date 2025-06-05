##!/usr/bin/python3
from UltraDict import UltraDict
import multiprocessing as mp
from time import time, sleep
import tkinter as tk
import numpy as np
import requests
from midi_emulator import MidiControllerEmulator
from midi_akai import class_akai
from rendering_engine import rendering_engine
from s2l_engine import sound_process
from server import WebSocketAPIServer
from randomizer import Randomizer


def autopilot():
    # Validate all presets
    # print("Validating presets...")
    # if not validate_all_presets():
    #     print("WARNING: Some presets failed validation!")
    # pass

    randomizer = Randomizer()
    starttime = time()
    
    while True:
        with state.lock:
            is_autopilot_on = state['autopilot']

        if is_autopilot_on:
            if time() - starttime > 2 + state['autopilot_time']:
                with state.lock:
                    randomizer.trigger()
                    starttime = time()
                requests.get("http://localhost:8000/api/update_state")
        else:
            # Reset timer when autopilot is off
            starttime = time()
            
        sleep(0.1)


def server():
    print('...starting gui server')
    server = WebSocketAPIServer()
    server.run()

def midi_devices():
    print('...starting midi thread')
    akai = class_akai()
    while True:
        # Small sleep to prevent CPU overload
        sleep(0.1)

    # use the following to activate on-screen midi emulator
    # root = tk.Tk()
    # midi = MidiControllerEmulator(root)
    # root.mainloop()

def rendering(state):
    print('...waiting for server...')
    # Wait for server to be ready
    sleep(2)

    print('...starting rendering thread')
    frame_renderer = rendering_engine()
    session = requests.Session()  # Reuse connection

    frame_interval = 1/30  # 30 FPS
    next_frame = time()

    while True:
        # Render frame
        frame_renderer.run(state)
        
        # Send frame data
        session.get("http://localhost:8000/api/update_cube")

        # Wait precisely until next frame
        next_frame += frame_interval
        sleep_time = next_frame - time()
        if sleep_time > 0:
            sleep(sleep_time)
        else:
            next_frame = time()  # Reset if we're falling behind


if __name__ == '__main__':
    # Unlink both shared memory buffers possibly used by UltraDict
    name = 'state'
    UltraDict.unlink_by_name(name, ignore_errors=True)
    UltraDict.unlink_by_name(f'{name}_memory', ignore_errors=True)

    state = UltraDict({
        "IO": False,
        "brightness": 1,
        "fade": 0,
        "autopilot": False,
        "autopilot_time": 3,
        "random": "all_elements",
        "s2l_values": [0.12, 0.2, 0.45, 0.7],
        "s2l_thresholds": [0, 0, 0, 0],
        "s2l_normalize": 10,
        "s2l_gain": 0.5,
        "s2l_update": True,
        "context": [0, 9],
        "midi_update": 0,
        "oneshot": 0,
        "crossfade_active": False,
        "numberOfChannels": 1,
        0: {
            "IO": True,
            "brightness": 0.9,
            "fade": 0.0,
            "update": True,
            9: {
                "name": "g_cube",
                "update": True,
                "params": ["size", "size", 3, 0.65, "surface", "sides", "Off", 0.45, "channel", "channel", "noS2l", 0.0, "speed", "speed", 3, 0.34]
            },
            "numberOfEffects": 1,
            0: {
                "name": "e_rainbow",
                "IO": True,
                "update": 1,
                "params": ["speed", "speed", 0.5, 0.1, "S2L Trigger", "Trigger", "Off", 0.1]
            }
        },

        # global effects channel
        9: {
            "update": True,
            "numberOfEffects": 1,
            0: {
                "name": "e_fade",
                "IO": True,
                "update": True,
                "params": ["amount", "amount", 0.5, 0.5],
            },
      },
    }, recurse=False, name=name, buffer_size=100000);

    try:
        global_memory_s2l  = mp.shared_memory.SharedMemory(create = True,name = "global_s2l_memory", size = 512)
    except FileExistsError:
        global_memory_s2l = mp.shared_memory.SharedMemory(name="global_s2l_memory")

    try:
        shared_cube_memory = mp.shared_memory.SharedMemory(name="cube_data", create=True, size=108000) # 9 channels, 1000 LEDs, RGB, 4 bytes per float32
    except FileExistsError:
        shared_cube_memory = mp.shared_memory.SharedMemory(name="cube_data")

    processes = [
        mp.Process(target=server, name="WebSocket/API Server", args=[]),
        mp.Process(target=sound_process, name="Sound Process", args=[]),
        mp.Process(target=midi_devices, name="MIDI Devices", args=[]),
        mp.Process(target=rendering, name="Renderer", args=[state]),
        mp.Process(target=autopilot, name="Autopilot", args=[])
    ]

    for proc in processes:
        proc.start()
        print(f'{proc.name}_Proc: {proc.pid}')

    for proc in processes:
        proc.join()


    global_memory_s2l.close()
    global_memory_s2l.unlink()
    shared_cube_memory.close()
    shared_cube_memory.unlink()

    print('done')
