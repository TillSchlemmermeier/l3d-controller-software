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
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np


#import MidiDevice
from MidiDevice import MidiDevice
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
    midifighter = MidiDevice(1,1)
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
        self.button_Open_MidiMon = QtWidgets.QPushButton("Open midi Monitor")
        self.button_StopR = QtWidgets.QPushButton("Stop Renderer")
        self.button_StartR.clicked.connect(self.start_Renderer)
        self.button_StopR.clicked.connect(self.stop_Renderer)
        self.button_Open_MidiMon.clicked.connect(self.show_Midimon)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button_StartR)
        layout.addWidget(self.button_StopR)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.button_Open_MidiMon)
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(layout)

        self.midi_thread = threading.Thread(name='midi', target=midi)
        self.rendering_thread = threading.Thread(name='render', target=rendering)

        #self.init_channelView_widget()
        #self.setCentralWidget(self.ChannelViewWidget)
        #layout.addWidget(self.ChannelViewWidget)

        self.init_midimonitor_widget(4,4)
        layout.addWidget(self.midimon_widget)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_midimonitor)
        timer.setInterval(30)
        timer.start()



    def start_download(self,info):
        self.list_widget.addItem(info)
    def start_Renderer(self):
        self.midi_thread.start()
        self.rendering_thread.start()
    def stop_Renderer(self):
        self.midi_thread.stop()
        self.rendering_thread.stop()
    def show_Midimon(self):
        self.midimon_widget.show()

    def init_midimonitor_widget(self,h,w):
        self.midimon_widget = QtWidgets.QWidget(self)
        grid = QtWidgets.QGridLayout(self)
        self.midimon_widget.setLayout(grid)
        self.midimon_titleStringArray =[[0 for x in range(w)] for y in range(h)]
        self.midimon_valueStringArray=[[0 for x in range(w)] for y in range(h)]
        for i in range(h):
            for j in range(w):
                self.midimon_titleStringArray[i][j] = QtWidgets.QLabel("Button : "+str(i)+" - "+str(j)+"\n")
                self.midimon_valueStringArray[i][j] = QtWidgets.QLabel("Midi: Channel : 2 Value 233")
                grid.addWidget(self.midimon_titleStringArray[i][j], i,j)
                grid.addWidget(self.midimon_valueStringArray[i][j], i,j)

    def init_channelView_widget(self):
        self.ChannelViewWidget = (QtWidgets.QWidget(self))
        grid = QtWidgets.QGridLayout(self)
        self.ChannelViewWidget.setLayout(grid)
        self.stringArray = []
        for i in range(4):
            self.stringArray.append(QtWidgets.QLabel("Channel "+str(i)))
            self.stringArray.append(QtWidgets.QLabel("Generator : DUMMY"))
            self.stringArray.append(QtWidgets.QLabel("Brightness : 127"))
            self.stringArray.append(QtWidgets.QLabel("Fade : 0"))
            self.stringArray.append(QtWidgets.QLabel("Shutter : 0"))
            self.stringArray.append(QtWidgets.QLabel("Parameter 1 : 89"))
            self.stringArray.append(QtWidgets.QLabel("Parameter 2 : 54"))
            self.stringArray.append(QtWidgets.QLabel("Parameter 3 : 110"))
            self.stringArray.append(QtWidgets.QLabel("Effect 1 : DUMMY"))
            self.stringArray.append(QtWidgets.QLabel("Parameter 1 : 0"))
            self.stringArray.append(QtWidgets.QLabel("Parameter 2 : 127"))
            self.stringArray.append(QtWidgets.QLabel("Parameter 3 : 110"))
            self.stringArray.append(QtWidgets.QLabel("Effect 2 : DUMMY"))
            self.stringArray.append(QtWidgets.QLabel("Parameter 1 : 0"))
            self.stringArray.append(QtWidgets.QLabel("Parameter 2 : 127"))
            self.stringArray.append(QtWidgets.QLabel("Parameter 3 : 110"))
            l=0
            for item in self.stringArray:
                grid.addWidget(item,l,i)
                l+=1

    def update_midimonitor(self):
        count=0
        for i in range(4):
            for j in range(4):
                self.midimon_valueStringArray[i][j].setText("Midi: "+str(count)+" - "+str(global_parameter[count]))
                count+=1


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
