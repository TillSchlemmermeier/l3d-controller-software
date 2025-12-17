#!/usr/bin/python3
import os
import sys
import struct
import socket
import pickle
import signal
import argparse
import tkinter as tk
from time import time, sleep
import multiprocessing as mp
from UltraDict import UltraDict

from randomizer import Randomizer
from s2l_engine import sound_process
from server import WebSocketAPIServer
from state_manager import StateManager
from rendering_engine import rendering_engine
from midi_launchcontrol import class_launchcontrol
from midi_emulator import MidiControllerEmulator

def autopilot(state, randomizer_queue):
    print('Starting autopilot / randomizer process')
    randomizer = Randomizer(state)
    randomizer.run_autopilot_loop(state, randomizer_queue)

def server(state, randomizer_queue):
    print('Starting FastAPI server')
    server = WebSocketAPIServer(state, randomizer_queue)
    server.run()

def midi_devices(state):
    print('...starting midi thread')
    launchcontrol = class_launchcontrol(state)
    # akai = class_akai(state)
    # fighter = class_fighter(state)
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
    # midi = MidiControllerEmulator(root, state)
    # root.mainloop()

def rendering(state):
    print('Starting rendering thread')
    frame_renderer = rendering_engine()

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_dest = ("127.0.0.1", 8001)

    frame_interval = 1/25  # 25 FPS
    next_frame = time()

    while True:
        # Render frame
        frame_renderer.run(state)
        
        # Send frame data
        udp_sock.sendto(b'trigger_cube_update', udp_dest)

        # Wait precisely until next frame
        next_frame += frame_interval
        sleep_time = next_frame - time()
        if sleep_time > 0:
            sleep(sleep_time)
        else:
            next_frame = time()  # Reset if we're falling behind


def backup_state(state):
    print("State backup process started, backing up every 30 seconds")
    while True:
        try:
            sleep(30)  # New backup every 30 seconds
            with state.lock:
                state_copy = dict(state)

            backup_file = os.path.join(f"state_backup.pkl")
            with open(backup_file, 'wb') as f:  # 'wb' for binary write
                pickle.dump(state_copy, f)
        except Exception as e:
            print(f"Backup error: {e}")


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
        StateManager(state).update_channel(channel_key)
    print("State restored from backup")

if __name__ == '__main__':
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
        "shift_activated": False,
        "oneshot": 0,
        "crossfade_active": False,
        "numberOfChannels": 1,
        0: {
            "IO": True,
            "brightness": 0.9,
            "fade": 0.0,
            "update": True,
            # generator element
            9: {
                "name": "g_cube",
                "update": True,
                "params": ['size', 'size', 4, 1.0, 'surface', 'sides', 'Off', 0.45, 'channel', 'channel', 'noS2L', 0.0, 'speed', 'speed', 0, 0.0]
            },
            "numberOfEffects": 0,
            # color element
            8: {
                'gradient': [[0, '#FF9F3F'], [100, '#0080FF']],
                'gradientType': 'linear',
                'speed': 0,
                'sectionStart': 0,
                'sectionWidth': 100,
                'rotateSpeedY': 50,
                'rotateSpeedZ': 50,
                'soundToLightOptions': [''],
                'update': True
            }
        },

        # global effects channel
        9: {
            "update": False,
            "numberOfEffects": 0,
      },
    }, recurse=False, name=name, buffer_size=1024 * 1024);

    if args.restore:
        restore_from_backup(state)

    try:
        global_memory_s2l  = mp.shared_memory.SharedMemory(create = True,name = "global_s2l_memory", size = 512)
        # Initialize buffer with zeros
        for i in range(0, 512, 8):
            global_memory_s2l.buf[i:i+8] = struct.pack('d', 0.0)
    except FileExistsError:
        global_memory_s2l = mp.shared_memory.SharedMemory(name="global_s2l_memory")

    try:
        shared_cube_memory = mp.shared_memory.SharedMemory(name="cube_data", create=True, size=108000) # 9 channels, 1000 LEDs, RGB, 4 bytes per float32
    except FileExistsError:
        shared_cube_memory = mp.shared_memory.SharedMemory(name="cube_data")

    # Create shared queue for randomizer process
    randomizer_queue = mp.Queue()

    processes = [
        mp.Process(target=server, name="WebSocket/API Server", args=[state, randomizer_queue]),
        mp.Process(target=sound_process, name="Sound Process", args=[state]),
        mp.Process(target=midi_devices, name="MIDI Devices", args=[state]),
        mp.Process(target=backup_state, name="State Backup", args=[state]),
        mp.Process(target=rendering, name="Renderer", args=[state]),
        mp.Process(target=autopilot, name="Autopilot", args=[state, randomizer_queue]),
    ]

    # Handler for graceful shutdown
    def signal_handler(sig, frame):
        # Only the main process should manage the child processes
        if mp.current_process().name == 'MainProcess':
            print(f"Received signal {sig}, shutting down...")
            # Terminate all child processes
            for proc in processes:
                if proc.is_alive():
                    print(f"Terminating {proc.name}...")
                    proc.terminate()
            sys.exit(0)
        else:
            # Child processes should just exit cleanly without trying to kill siblings
            sys.exit(0)

    # Register the signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    for proc in processes:
        proc.start()
        print(f'{proc.name} process started with PID {proc.pid}')

    try:
        for proc in processes:
            proc.join()
    except (KeyboardInterrupt, SystemExit):
        print("Main process exited")
    finally:
        # Ensure all processes are definitely dead
        for proc in processes:
            if proc.is_alive():
                proc.terminate()
                proc.join(timeout=1.0)

        # Clean up shared memory
        try:
            global_memory_s2l.close()
            global_memory_s2l.unlink()
            shared_cube_memory.close()
            shared_cube_memory.unlink()
            print("Shared memory cleaned up")
        except Exception as e:
            print(f"Error cleaning up shared memory: {e}")
