#!/usr/bin/python3
import logging
import sys
from datetime import datetime
from UltraDict import UltraDict
import multiprocessing as mp
from time import time, sleep
import tkinter as tk
import requests
from midi_emulator import MidiControllerEmulator
from midi_akai import class_akai
from midi_fighter import class_fighter
from midi_launchcontrol import class_launchcontrol
from rendering_engine import rendering_engine
from s2l_engine import sound_process
from server import WebSocketAPIServer
from randomizer import Randomizer
from state_manager import StateManager
import pickle
import argparse
import os

def setup_complete_logging():
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f'logs/l3d_controller_{timestamp}.log'

    # Open log file for writing
    log_file = open(log_filename, 'w', buffering=1)  # Line buffered

    # Create tee objects with all required methods
    class TeeOutput:
        def __init__(self, file_obj, original_stream):
            self.file = file_obj
            self.original = original_stream

        def write(self, text):
            self.file.write(text)
            self.original.write(text)

        def flush(self):
            self.file.flush()
            self.original.flush()

        def isatty(self):
            """Check if the original stream is a TTY"""
            return self.original.isatty()

        def fileno(self):
            """Return file descriptor of original stream"""
            return self.original.fileno()

        def __getattr__(self, name):
            """Delegate any other attributes to the original stream"""
            return getattr(self.original, name)

    # Redirect stdout and stderr
    sys.stdout = TeeOutput(log_file, sys.__stdout__)
    sys.stderr = TeeOutput(log_file, sys.__stderr__)

    # Also setup structured logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )

    print(f"L3D Controller started - Log file: {log_filename}")
    return log_filename, log_file

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
    logging.info('Starting GUI server')
    server = WebSocketAPIServer()
    server.run()

def midi_devices(state):
    logging.info('...starting midi thread')
    launchcontrol = class_launchcontrol()
    # akai = class_akai()
    # fighter = class_fighter()
    # fighter.update()

    while True:
        # Small sleep to prevent CPU overload
        if state['midi_update'] == True:
            launchcontrol.update()
            with state.lock:
                state['midi_update'] = False

        sleep(0.1)

    # use the following to activate on-screen midi emulator
    # root = tk.Tk()
    # midi = MidiControllerEmulator(root)
    # root.mainloop()

def rendering(state):
    logging.info('Waiting for server...')
    sleep(2)

    logging.info('Starting rendering thread')
    frame_renderer = rendering_engine()
    session = requests.Session()  # Reuse connection

    frame_interval = 1/25  # 25 FPS
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


def backup_state(state):
    while True:
        try:
            sleep(30)  # New backup every 30 seconds
            with state.lock:
                state_copy = dict(state)

            backup_file = os.path.join(f"state_backup.pkl")
            with open(backup_file, 'wb') as f:  # 'wb' for binary write
                pickle.dump(state_copy, f)
            logging.info("State backup created")
        except Exception as e:
            logging.error(f"Backup error: {e}")


def restore_from_backup(state):
    backup_file = os.path.join(f"state_backup.pkl")
    with open(backup_file, 'rb') as f:  # Note: 'rb' for binary read
        backup_state = pickle.load(f)

    with state.lock:
        state.clear()
        state.update(backup_state)
        state.apply_update()

    channel_indices = list(range(state['numberOfChannels'])) + [9]
    for channel_key in channel_indices:
        StateManager().update_channel(channel_key)
    logging.info("State restored from backup")

if __name__ == '__main__':
    log_file_path, log_file_handle = setup_complete_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument('--restore', action='store_true')
    args = parser.parse_args()

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
        "s2l_normalize": False,
        "s2l_gain": 0.5,
        "s2l_update": True,
        "context": [[0, 9], [0, 0], [0 ,0], [0 ,0]],
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

    if args.restore:
        restore_from_backup(state)

    try:
        global_memory_s2l  = mp.shared_memory.SharedMemory(create = True,name = "global_s2l_memory", size = 512)
        # Initialize buffer with zeros in string format
        for i in range(0, 512, 8):
            global_memory_s2l.buf[i:i+8] = '0.0'.encode('utf-8').ljust(8, b'\x00')
    except FileExistsError:
        global_memory_s2l = mp.shared_memory.SharedMemory(name="global_s2l_memory")

    try:
        shared_cube_memory = mp.shared_memory.SharedMemory(name="cube_data", create=True, size=108000) # 9 channels, 1000 LEDs, RGB, 4 bytes per float32
    except FileExistsError:
        shared_cube_memory = mp.shared_memory.SharedMemory(name="cube_data")

    processes = [
        mp.Process(target=server, name="WebSocket/API Server", args=[]),
        mp.Process(target=sound_process, name="Sound Process", args=[]),
        mp.Process(target=midi_devices, name="MIDI Devices", args=[state]),
        mp.Process(target=backup_state, name="State Backup", args=[state]),
        mp.Process(target=rendering, name="Renderer", args=[state]),
        mp.Process(target=autopilot, name="Autopilot", args=[]),
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


    logging.info('Application shutdown complete')
    if log_file_handle:
        log_file_handle.close()
