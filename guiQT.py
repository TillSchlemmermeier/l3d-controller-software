#!/usr/bin/python3
import threading
import time
# import rendering class
from rendering_engine import rendering_engine
# import global variable
from global_parameter_module import global_parameter

import sys
import tempfile
import subprocess
import time
from random import randint
import urllib.request
from PyQt5 import QtWidgets, QtGui
#from PyQt5.QtCore import QObject,QThread, pyqtSigna
#from mainwindow import Ui_MainWindow
MidiKey=0
MidiValue=0
MidiChannel=0


def midi():
    '''
    Midi Thread
    '''
    i = 0
    print('Waiting some time to start cube...')
    while True:
        print('Some midi input...')
        if i == 5:
            print('Starting cube...')
            # write some values into array to simulate midi input
            global_parameter[0] = 1     # staring cube
            global_parameter[1] = 200   # set brightness
            global_parameter[3] = 200   # set brightness limiter
            global_parameter[40] = 1    # activate channel 1

        if i == 10:
            global_parameter[20] = 1    # select g_random

        i += 1
        time.sleep(1)


def rendering():
    '''
    rendering thread
    '''

    # start rendering engine
    frame_renderer = rendering_engine(log=True)
    while True:
        # long sleeping time, so logfile is not flooded
        time.sleep(2)
        # render frame
        frame_renderer.run()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        global MidiKey
        global MidiValue
        global MidiChannel

        self.list_widget = QtWidgets.QListWidget()
        self.button_StartR = QtWidgets.QPushButton("Start Renderer")
        self.button_StopR = QtWidgets.QPushButton("Stop Renderer")
        self.button_StartR.clicked.connect(self.start_Renderer)
        self.button_StopR.clicked.connect(self.stop_Renderer)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button_StartR)
        layout.addWidget(self.button_StopR)
        layout.addWidget(self.list_widget)
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(layout)

        self.midi_thread = threading.Thread(name='midi', target=midi)
        self.rendering_thread = threading.Thread(name='render', target=rendering)


    def start_download(self,info):
        self.list_widget.addItem(info)
    def start_Renderer(self):
        self.midi_thread.start()
        self.rendering_thread.start()
    def stop_Renderer(self):
        self.midi_thread.stop()
        self.rendering_thread.stop()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
