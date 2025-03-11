##!/usr/bin/python3
import time
# from rendering_engine import rendering_engine
from rendering_engine_2d import rendering_engine_2d
from rendering_engine_visualization import rendering_engine_visualization
# import global variable
#from global_parameter_module import global_parameter
from copy import deepcopy
import sys
#import urllib.request
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication 

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

import numpy as np
from ctypes import c_char, c_char_p

from midi import class_midi
from midi_emulator import MidiControllerEmulator
from time import sleep
from time import time as tottime
import multiprocessing as mp
from s2l_engine import sound_process
from random import choice
from server import class_gui_server
from UltraDict import UltraDict
import requests
import json
import tkinter as tk

class CubeDataSharedMemory:
    def __init__(self):
        self.shape = (9, 1000, 4)  # 9 channels, 1000 LEDs, RGBA
        self.size = np.prod(self.shape) * 4  # 4 bytes per float32
        try:
            self.shm = mp.shared_memory.SharedMemory(name="cube_data", create=True, size=self.size)
        except FileExistsError:
            self.shm = mp.shared_memory.SharedMemory(name="cube_data")
        
        self.array = np.ndarray(self.shape, dtype=np.float32, buffer=self.shm.buf)    

def autopilot(state):
    pass
    # starttime = tottime()
    # with open('global_presets.dat', 'r') as file:
    #     presets = file.readlines()

    # preset = choice(presets)

    # while True:
    #     time.sleep(0.5)
    #     if state['autopilot'] == 1:
    #         print('active autopilot')
            # starttime = tottime()
            # while True:
            #     if tottime()-starttime > 2+float(state['autopilot-time'])*180:
            #         preset = choice(presets).strip('\n').split()
            #         print('new preset: ', preset[0])

            #         for i, value in zip(range(20,159), preset[1:]):
            #             array[i] = float(value)

            #         starttime = tottime()

            #     time.sleep(0.1)
            #     if state['autopilot'] == 0:
            #         print('stopping autopilot')
            #         break

def midi_arduino(state):
    print('...starting arduino midi')
    pass
    # while True:
    #     print(state['CH1']['generator']['update'])
    #     time.sleep(1)
    # # arduino = class_arduino_midi(array)
    # arduino.run()

def gui_server(state):
    print('...starting gui server')
    server = class_gui_server(state)
    server.run()

def midi_devices(state):
    '''
    Midi Thread
    '''
    print('...starting midi thread')
    # we should do something to detect ports! -> YES we should :)
    # midi = class_midi(state)
    root = tk.Tk()
    midi = MidiControllerEmulator(root)
    root.mainloop()
    # while True:
    #     time.sleep(0.1)
    #     if state['midi_update'] == 1:
    #         print('update midi')
    #         midi.update_midi()
    #         state['midi_update'] = 0


def rendering(array, label, pause_time = 0.03, log = False):
    '''
    Rendering Thread
    '''
    print('...starting rendering thread')

    if log == True:
        print('...is logging')
        # long sleeping time, so logfile is not flooded
        pause_time = 2

    # initialize window
    # app = QtGui.QApplication([])
    app = QtWidgets.QApplication([])
    window = gl.GLViewWidget()
    window.setWindowTitle('L3D Cube')
    screen_resolution = app.desktop().screenGeometry()
    width = screen_resolution.width()
    # x coordinate, y coordinate, xsize, ysize
    # window.setGeometry(width + 1, 0, 1080, 1200)
    window.setGeometry(width + 1, 0, 600, 600)
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    #window.setCameraPosition(pos = None, distance = 15, elevation = 30, azimuth = 0)
    window.opts['distance'] = 30
    window.opts['azimuth'] = 40
    window.opts['elevation'] = 30
    window.opts['fov'] = 30
    window.show()

    # get positions for scatter plot
    pos = []
    for z in range(10):
        for x in range(10):
            for y in range(10):
                pos.append([x, y, 9-z])

    pos = np.array(pos)
    # pos-4.5 to center cube
    scatterplot = gl.GLScatterPlotItem(pos = pos-4.5, size = 10)
    window.addItem(scatterplot)

    # start rendering engine
    frame_renderer = rendering_engine(array, label, log)

    '''
    while True:
        time.sleep(pause_time)
        # render frame
        colors = frame_renderer.run()
        scatterplot.setData(color = colors)
    '''
    def update():
        colors = frame_renderer.run()
        colors[:, :] += 0.05
        #colors[0, 0] = 0.0
        #colors[1, 1] = 0.0
        #colors[8, 2] = 0.0


        scatterplot.setData(color = np.clip(colors, 0, 1))

    t = QtCore.QTimer()
    t.timeout.connect(update)
    t.start(1)
    # QtGui.QApplication.instance().exec_()
    QApplication.instance().exec_()



def rendering_visualize(state, pause_time = 0.1, log = False):
    '''
    Rendering Thread to visualize cube
    '''
    time.sleep(3)
    print('...starting rendering thread')

    # initialize window
    # app = QtGui.QApplication([])
    app = QApplication([])
    # window = gl.GLViewWidget()
    # window.setWindowTitle('L3D Cube')
    # screen_resolution = app.desktop().screenGeometry()
    # width = screen_resolution.width()
    # # x coordinate, y coordinate, xsize, ysize
    # window.setGeometry(width + 1, 0, 1080, 1200)
    # window.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    # window.opts['distance'] = 30
    # window.opts['azimuth'] = 40
    # window.opts['elevation'] = 30
    # window.opts['fov'] = 30

    # window.show()
    # #g = gl.GLGridItem()
    # #window.addItem(g)

    # # get positions for scatter plot
    # pos = []
    # for z in range(10):
    #     for x in range(10):
    #         for y in range(10):
    #             pos.append([x, y, 9-z])

    # pos = np.array(pos)
    # # pos-4.5 to center cube
    # scatterplot = gl.GLScatterPlotItem(pos = pos-4.5, size = 20)
    # window.addItem(scatterplot)

    # start rendering engine
    frame_renderer = rendering_engine_visualization(state, log)

    # cubedata_memory  = mp.shared_memory.SharedMemory(name = "cubedata")
    shared_mem = CubeDataSharedMemory()

    def update():
        # Get array of shape (9, 1000, 4) containing combined cube and channel data
        all_colors = frame_renderer.run(state)
        np.copyto(shared_mem.array, all_colors)
        # all_colors[:, :, :] += 0.05
        # Send the data to the frontend
        # data = {
        #     "type": "cube_data",
        #     "data": all_colors.tolist()
        # }
        requests.post(
            "http://localhost:8000/api/stream", 
            json= { "type": "cube_data", "data": [] }, 
            headers={ "Content-Type": "application/json" }
        )

        # Update the 3D visualization with just the combined cube data (first element)
        # scatterplot.setData(color=np.clip(all_colors[0], 0, 1))


    t = QtCore.QTimer()
    t.timeout.connect(update)
    t.start(200)
    QApplication.instance().exec_()


    #while True:
    #    time.sleep(pause_time)
        # render frame
    #    frame_renderer.run()


def rendering_2d(array, label, pause_time = 0.03, log = False):
    '''
    Rendering Thread
    '''
    print('...starting rendering thread')

    if log == True:
        print('...is logging')
        # long sleeping time, so logfile is not flooded
        pause_time = 2

    # start rendering engine
    frame_renderer = rendering_engine_2d(array, label, [10, 10],log)

    while True:
        time.sleep(pause_time)
        # render frame
        frame_renderer.run()


if __name__ == '__main__':
    # define global variables

    manager = mp.Manager()
    # Unlink both shared memory buffers possibly used by UltraDict
    name = 'state'
    UltraDict.unlink_by_name(name, ignore_errors=True)
    UltraDict.unlink_by_name(f'{name}_memory', ignore_errors=True)

    state = UltraDict({
        "IO": 1,
        "brightness": 1,
        "fade": 0,
        "brightness-limiter": 1,
        "autopilot": 1,
        "autopilot-time": 0.02,
        "s2l_values": [0.12, 0.2, 0.45, 0.7],
        "s2l_thresholds": [0, 0, 0, 0],
        "s2l_normalize": 10,
        "s2l_gain": 0.5,
        "context": [0, 9],
        "midi_update": 0,
        "midi_values": {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
        },
        "numberOfChannels": 1,
        0: {
            "IO": 1,
            "brightness": 0.9,
            "fade": 0.65,
            "update": 1,
            "generator": {
                "name": "g_cube",
                "update": 1,
                "params": ["size", "size", 3, 0.65, "surface", "sides", "Off", 0.45, "channel", "channel", "Trigger", 0.65, "speed", "speed", 9, 0.2]
            },
            "effects": [{
                "name": "e_rainbow",
                "IO": 1,
                "update": 1,
                "params": ["speed", "speed", 0.5, 0.1, "", "", "", "", "", "", "", "", "S2L Trigger", "Trigger", "Off", 0.1]
            }],
        },
        1: {
            "IO": 0,
            "brightness": 0.0,
            "fade": 0.0,
            "update": 0,
            "generator": {
                "name": "",
                "params": [],
            },
            "effects": [],
        },
        # global effects channel
        9: {
            "IO": 1,
            "update": 1,
            "effects": [
                {
                    "name": "e_fade",
                    "IO": 1,
                    "update": True,
                    "params": ["amount", "amount", 0.5, 0.5, "", "", "", "", "", "", "", "", "channel", "channel", "3", 0.7],
                },
                {
                    "name": "e_fade",
                    "IO": 1,
                    "update": True,
                    "params": ["amount", "amount", 0.5, 0.5, "", "", "", "", "", "", "", "", "channel", "channel", "3", 0.7],
                }
            ],
      },
      "oneShots": [],
    }, recurse=False, name=name, buffer_size=100_000);
    
    # Create a queue for communication
    queue = mp.Queue()

    try:
        global_memory_s2l = mp.shared_memory.SharedMemory(name="global_s2l_memory")
    except:
        global_memory_s2l  = mp.shared_memory.SharedMemory(create = True,name = "global_s2l_memory", size = 512)




    # try:
    #     cubedata_memory  = mp.shared_memory.SharedMemory(name = "cubedata")
    # except:
    #     cubedata_memory  = mp.shared_memory.SharedMemory(create = True,name = "cubedata", size = 32000)
    

    if len(sys.argv) >= 2:
        if sys.argv[1] == '--2d':
            proc_renderer = mp.Process(target=rendering_2d, args = [global_parameter, global_label])
            mode = '2d'
        elif sys.argv[1] == '--visualize':
            print('visualize')
            proc_renderer = mp.Process(target=rendering_visualize, args = [state])
            mode = '3d'
        else:
            print('default mode 1')
            mode = '3d'
            proc_renderer = mp.Process(target=rendering, args = [global_parameter, global_label])
    else:
        mode = '3d'
        print('default mode')
        proc_renderer = mp.Process(target=rendering, args = [global_parameter, global_label])

    # assign processes
    proc_gui_server = mp.Process(target = gui_server, args = [state])
    proc_midi = mp.Process(target=midi_devices, args = [state])
    proc_arduino = mp.Process(target=midi_arduino, args = [state])
    proc_sound = mp.Process(target = sound_process, args = [])
    proc_autopilot = mp.Process(target = autopilot, args = [state])

    # if test modus, load last temporary preset
    if len(sys.argv) >= 2:
        if sys.argv[1] == '--test':
            print(' test mode - loading temporary preset')
            with open('temporary_presets.dat') as file:
                presets = file.readlines()

            try:
                indices = []
                indices.append([20, 21, 22, 23] + [x for x in range( 40, 70)])
                preset = presets[-1].strip('\n').split()
                print('loading preset', preset[0])

                # write values into global parameter array
                # hopefully on the right place
                for i, value in zip(indices[0], preset[1:]):
                    # dont set channel on/off
                    if i not in [40, 70, 100, 130]:
                        global_parameter[i] = float(value)
            except:
                print('error loading temporary preset')

    # starting processes
    print('start')
    proc_midi.start()
    print('MIDI_Proc :'+ str(proc_midi.pid))
    # proc_arduino.start()
    # print('ARDUINO_Proc :'+ str(proc_arduino.pid))
    proc_renderer.start()
    print('RENDERER_Proc :'+ str(proc_renderer.pid))
    proc_autopilot.start()
    print('AUTO_Proc :'+ str(proc_autopilot.pid))
    proc_gui_server.start()
    print('GUI_Proc :'+ str(proc_gui_server.pid))
    proc_sound.start()
    print('SOUND_Proc :'+ str(proc_sound.pid))


#    time.sleep(1)
    proc_midi.join()
    # proc_arduino.join()
    proc_renderer.join()
    proc_gui_server.join()
    proc_sound.join()
    proc_autopilot.join()

    # global_memory.close()
    global_memory_s2l.close()
    # global_memory.unlink()
    global_memory_s2l.unlink()

    # TODO FIX THIS
    # shared_mem.close()
    # shared_mem.unlink()

    print('done')
