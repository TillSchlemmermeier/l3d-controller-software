##!/usr/bin/python3
#import threading    # do we need this or is QT taking care of everything?
import time
# import rendering class
from rendering_engine import rendering_engine
from rendering_engine_2d import rendering_engine_2d
# import global variable
#from global_parameter_module import global_parameter
from copy import deepcopy
import sys
#import tempfile     # what is this?
#import subprocess   # obsolete?
#import urllib.request
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
from ctypes import c_char, c_char_p

from midi_akai import class_akai
from midi_fighter import class_fighter
from midi_launchpad import class_launchpad_mk3
from midi_arduino import class_arduino_midi
from gui_class import MainWindow
from artnet_interface import class_artnet
from time import sleep
from time import time as tottime
import multiprocessing as mp
from s2l_engine import sound_process
from random import choice

#from PyQt5.QtCore import QObject,QThread, pyqtSigna
#from mainwindow import Ui_MainWindow

def autopilot(array):

    starttime = tottime()
    with open('global_presets.dat', 'r') as file:
        presets = file.readlines()

    preset = choice(presets)

    while True:
        time.sleep(0.5)
        if array[5] == 1:
            print('active autopilot')
            starttime = tottime()
            while True:
                if tottime()-starttime > 2+float(array[6])*20:
                    print('new preset')
                    preset = choice(presets).strip('\n').split()

                    for i, value in zip(range(20,159), preset[1:]):
                        array[i] = float(value)

                    starttime = tottime()

                time.sleep(0.1)
                if array[5] == 0:
                    print('stopping autopilot')
                    break

def midi_arduino(array):
    print('...starting arduino midi')
    arduino = class_arduino_midi(array)
    arduino.run()

def midi_devices(array):
    '''
    Midi Thread
    '''
    print('...starting midi thread')
    # we should do something to detect ports! -> YES we should :)
    midifighter = class_fighter(array)
    launchpad = class_launchpad_mk3(array)
    akai = class_akai(array)

    temptime = tottime()
    temp_param = [0 for i in range(255)]
    temp_param[:] = array[:]
    while True:
        time.sleep(0.5)

        # check for changes
        # that is, selection of generators/effects
        for i in range(4):
            if array[20+5*i:25+5*i] != temp_param[20+5*i:25+5*i]:
                if array[20+5*i] != temp_param[20+5*i]:
                    array[201+i] = 0
                    midifighter.event(['T', i, 0])
                elif array[21+5*i] != temp_param[21+5*i]:
                    array[201+i] = 1
                    midifighter.event(['T', i, 1])
                elif array[22+5*i] != temp_param[22+5*i]:
                    array[201+i] = 2
                    midifighter.event(['T', i, 2])
                elif array[23+5*i] != temp_param[23+5*i]:
                    midifighter.event(['T', i, 3])
                    array[201+i] = 3

        # check whether the glbaol effects menu was openend
        if array[230] ==  1:
            array[230] = 0
            midifighter.event(['T', 0, 4])
            midifighter.event(['T', 1, 5])
            midifighter.event(['T', 2, 6])
            midifighter.event(['T', 3, 7])

        temp_param[:] = array[:]

        # pass

def artnet_process(array):
    a = class_artnet(array)

    while True:
        a.run()
        sleep(0.01)


def rendering(array, label, pause_time = 0.03, log = False):
    '''
    Rendering Thread
    '''
    print('...starting rendering thread')

    if log == True:
        print('...is logging')
        # long sleeping time, so logfile is not flooded
        pause_time = 2

    # start rendering engine
    frame_renderer = rendering_engine(array, label, log)

    while True:
        time.sleep(pause_time)
        # render frame
        frame_renderer.run()

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

def gui(array, label, mode):
    '''main routine'''
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(array, label, mode)
    #window.resize(640, 480)
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # define global variables
    global_parameter = mp.Array('d', [0 for x in range(255)])
    global_label     = mp.Array(c_char_p, 120)
    global_memory   = mp.shared_memory.SharedMemory(create = True,name = "GuiValues1", size = 640)
    global_memory_s2l   = mp.shared_memory.SharedMemory(create = True,name = "global_s2l_memory", size = 512)

    for i in range(100):
        global_label[i] = b'init'

    # start values for s2l_engine
    global_parameter[10] = 0.1
    global_parameter[11] = 0.2
    global_parameter[12] = 0.45
    global_parameter[13] = 0.7

    if len(sys.argv) >= 2:
        if sys.argv[1] == '--2d':
            proc_renderer = mp.Process(target=rendering_2d, args = [global_parameter, global_label])
            mode = '2d'
        else:
            mode = '3d'
            proc_renderer = mp.Process(target=rendering, args = [global_parameter, global_label])
    else:
        mode = '3d'
        proc_renderer = mp.Process(target=rendering, args = [global_parameter, global_label])

    # assign processes
    proc_midi = mp.Process(target=midi_devices, args = [global_parameter])
    proc_arduino = mp.Process(target=midi_arduino, args = [global_parameter])
    proc_gui = mp.Process(target=gui, args = [global_parameter, global_label, mode])
    # proc_artnet = mp.Process(target=artnet_process, args = [global_parameter])
    proc_sound = mp.Process(target = sound_process, args = [global_parameter])
    proc_autopilot = mp.Process(target = autopilot, args = [global_parameter])

    # if test modus, load last temporary preset
    if len(sys.argv) >= 2:
        if sys.argv[1] == '--test':
            print(' test mode - loading temporary preset')
            with open('temporary_preset.dat') as file:
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
    proc_arduino.start()
    proc_renderer.start()
    proc_autopilot.start()
    proc_gui.start()
    proc_sound.start()
    # proc_artnet.start()

#    time.sleep(1)
    proc_midi.join()
    proc_arduino.join()
    proc_renderer.join()
    proc_gui.join()
    proc_sound.join()
    proc_autopilot.join()
#    proc_artnet.join()

    global_memory.close()
    global_memory_s2l.close()
    global_memory.unlink()
    global_memory_s2l.unlink()

    print('done')
s
