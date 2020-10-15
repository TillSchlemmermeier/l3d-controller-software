##!/usr/bin/python3
#import threading    # do we need this or is QT taking care of everything?
import time
# import rendering class
from rendering_engine import rendering_engine
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

from MidiDevice import class_fighter, class_akai, class_launchpad_mk3
from gui_class import MainWindow
from artnet_interface import class_artnet
from time import sleep
import multiprocessing as mp
from s2l_engine import sound_process

#from PyQt5.QtCore import QObject,QThread, pyqtSigna
#from mainwindow import Ui_MainWindow


def midi_devices(array):
    '''
    Midi Thread
    '''
    print('...starting midi thread')
    # we should do something to detect ports! -> YES we should :)
    midifighter = class_fighter(array)
    launchpad = class_launchpad_mk3(array)
    akai = class_akai(array)

    while True:
        time.sleep(1)
        pass

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

def gui(array,label):
    '''main routine'''
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(array,label)
    #window.resize(640, 480)
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # define global variables
    global_parameter = mp.Array('d', [0 for x in range(255)])
    global_label     = mp.Array(c_char_p, 100)
    global_memory   = mp.shared_memory.SharedMemory(create = True,name = "GuiValues1", size = 512)
    global_memory_s2l   = mp.shared_memory.SharedMemory(create = True,name = "global_s2l_memory", size = 512)

    for i in range(100):
        global_label[i] = b'init'

    # start values for s2l_engine
    global_parameter[10] = 0.1
    global_parameter[11] = 0.2
    global_parameter[12] = 0.45
    global_parameter[13] = 0.7

    # assign processes
    proc_midi = mp.Process(target=midi_devices, args = [global_parameter])
    proc_renderer = mp.Process(target=rendering, args = [global_parameter, global_label])
    proc_gui = mp.Process(target=gui, args = [global_parameter,global_label])
    # proc_artnet = mp.Process(target=artnet_process, args = [global_parameter])
    proc_sound = mp.Process(target = sound_process, args = [global_parameter])

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

    proc_renderer.start()

    proc_gui.start()
    proc_sound.start()
    # proc_artnet.start()

#    time.sleep(1)
    proc_midi.join()
    proc_renderer.join()
    proc_gui.join()
    proc_sound.join()
#    proc_artnet.join()

    global_memory.close()
    global_memory_s2l.close()
    global_memory.unlink()
    global_memory_s2l.unlink()

    print('done')
s
