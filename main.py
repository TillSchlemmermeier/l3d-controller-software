##!/usr/bin/python3
#import threading    # do we need this or is QT taking care of everything?
import time
# import rendering class
from rendering_engine import rendering_engine
# import global variable
#from global_parameter_module import global_parameter
from copy import deepcopy
import sys
import tempfile     # what is this?
import subprocess   # obsolete?
#import urllib.request
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np

from MidiDevice import class_fighter, class_akai
from gui_class import MainWindow

import multiprocessing as mp

#from PyQt5.QtCore import QObject,QThread, pyqtSigna
#from mainwindow import Ui_MainWindow


def midi_fighter(array):
    '''
    Midi Thread
    '''
    print('...starting midi thread')
    # we should do something to detect ports! -> YES we should :)
    midifighter = class_fighter(array)
    # launchpad = class_akai()

    while True:
        time.sleep(1)
        pass

def rendering(array, pause_time = 0.03, log = False):
    '''
    Rendering Thread
    '''
    print('...starting rendering thread')

    if log == True:
        print('...is logging')
        # long sleeping time, so logfile is not flooded
        pause_time = 2

    # start rendering engine

    frame_renderer = rendering_engine(array, log)

    while True:
        time.sleep(pause_time)
        # render frame
        frame_renderer.run()

def gui(array):
    """main routine
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(array)
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    global_parameter = mp.Array('d', [0 for x in range(255)])
    #self.rendering_thread.start()

    '''
    with mp.Pool(processes=3) as pool:
        gui = pool.apply_async(gui(global_parameter))
        midi = pool.apply_async(midi_fighter(global_parameter))
        render = pool.apply_async(rendering(global_parameter))




    print('Done')

    '''

    proc_midi = mp.Process(target=midi_fighter, args = [global_parameter])
    proc_renderer = mp.Process(target=rendering, args = [global_parameter])
    proc_gui = mp.Process(target=gui, args = [global_parameter])
    print('start');
    proc_midi.start();
    proc_renderer.start()
    proc_gui.start()
    time.sleep(1)
    proc_midi.join();
    self.proc_renderer.join();
    proc_gui.join();
    print('done')
