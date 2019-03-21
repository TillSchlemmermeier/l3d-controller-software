#!/usr/bin/python3
import threading    # do we need this or is QT taking care of everything?
import time
# import rendering class
from rendering_engine import rendering_engine
# import global variable
from global_parameter_module import global_parameter

import sys
import tempfile     # what is this?
import subprocess   # obsolete?
#import urllib.request
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np


from MidiDevice import class_fighter
#from PyQt5.QtCore import QObject,QThread, pyqtSigna
#from mainwindow import Ui_MainWindow


def midi():
    '''
    Midi Thread
    '''
    print('...starting midi thread')
    # we should do something to detect ports! -> YES we should :)
    midifighter = class_fighter(in_port = 2,out_port = 2)


def rendering(pause_time = 2, log = True):
    '''
    Rendering Thread
    '''

    if log == True:
        # long sleeping time, so logfile is not flooded
        pause_time = 2

    # start rendering engine
    frame_renderer = rendering_engine(log)
    while True:
        time.sleep(pause_time)
        # render frame
        frame_renderer.run()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        #global MidiKey
        #global MidiValue
        #global MidiChannel

        # initialize layout
        # creating main container-frame, parent it to QWindow
        self.main_CF = QtWidgets.QFrame(self)
        self.main_CF.setStyleSheet('background-color: rgba(150, 0, 0, 1);')
        self.setCentralWidget(self.main_CF)
        # creating layout and parent it to main container
        # is it correct, that main_CL now manages children of main_CF ?
        self.main_CL = QtWidgets.QVBoxLayout(self.main_CF)

        # creating the first subcontainer + layout, parenting it
        control_CGF = QtWidgets.QFrame(self.main_CF)
        self.main_CL.addWidget(control_CGF)
        control_CGF.setStyleSheet('background-color: rgba(150, 150, 0, 1);')
        control_CGL = QtWidgets.QHBoxLayout(control_CGF)

        # creating the second subcontainer + layout, parenting it
        launchpad_CGF = QtWidgets.QFrame(self.main_CF)
        self.main_CL.addWidget(launchpad_CGF)
        launchpad_CGF.setStyleSheet('background-color: rgba(0, 150, 0, 1);')
        launchpad_CGL = QtWidgets.QHBoxLayout(launchpad_CGF)

        # doing the same with a third container
        fighter_CGF = QtWidgets.QFrame(self.main_CF)
        self.main_CL.addWidget(fighter_CGF)
        fighter_CGF.setStyleSheet('background-color: rgba(150, 150, 150, 1);')
        self.fighter_CGL = QtWidgets.QHBoxLayout(fighter_CGF)
        # SUB containers for fighter channels 1-4
        fi_ch1_CGF = QtWidgets.QFrame(fighter_CGF)
        self.fighter_CGL.addWidget(fi_ch1_CGF)
        fi_ch1_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        fi_ch1_CGL = QtWidgets.QVBoxLayout(fi_ch1_CGF)

        fi_ch2_CGF = QtWidgets.QFrame(fighter_CGF)
        self.fighter_CGL.addWidget(fi_ch2_CGF)
        fi_ch2_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        fi_ch2_CGL = QtWidgets.QVBoxLayout(fi_ch2_CGF)

        fi_ch3_CGF = QtWidgets.QFrame(fighter_CGF)
        self.fighter_CGL.addWidget(fi_ch3_CGF)
        fi_ch3_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        fi_ch3_CGL = QtWidgets.QVBoxLayout(fi_ch3_CGF)

        fi_ch4_CGF = QtWidgets.QFrame(fighter_CGF)
        self.fighter_CGL.addWidget(fi_ch4_CGF)
        fi_ch4_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        fi_ch4_CGL = QtWidgets.QVBoxLayout(fi_ch4_CGF)
####
        self.button_StartR = QtWidgets.QPushButton("Start Renderer")
        self.button_StopR = QtWidgets.QPushButton("Stop Renderer")
        self.button_StartR.clicked.connect(self.start_Renderer)
        self.button_StopR.clicked.connect(self.stop_Renderer)

        control_CGL.addWidget(self.button_StartR)
        control_CGL.addWidget(self.button_StopR)
###
        self.stringArray_ch1 = []
        self.stringArray_ch1.append(QtWidgets.QLabel("Channel 1"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Generator : DUMMY"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Brightness : 127"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Fade : 0"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Shutter : 0"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 1 : 89"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 2 : 54"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Effect 1 : DUMMY"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Effect 2 : DUMMY"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 3 : 110"))


        for item in self.stringArray_ch1:
            fi_ch1_CGL.addWidget(item)
#
        self.stringArray_ch2 = []
        self.stringArray_ch2.append(QtWidgets.QLabel("Channel 2"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Generator : DUMMY"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Brightness : 127"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Fade : 0"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Shutter : 0"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 1 : 89"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 2 : 54"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Effect 1 : DUMMY"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Effect 2 : DUMMY"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 3 : 110"))


        for item in self.stringArray_ch2:
            fi_ch2_CGL.addWidget(item)
#
        self.stringArray_ch3 = []
        self.stringArray_ch3.append(QtWidgets.QLabel("Channel 3"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Generator : DUMMY"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Brightness : 127"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Fade : 0"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Shutter : 0"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 1 : 89"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 2 : 54"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Effect 1 : DUMMY"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Effect 2 : DUMMY"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 3 : 110"))


        for item in self.stringArray_ch3:
            fi_ch3_CGL.addWidget(item)
#
        self.stringArray_ch4 = []
        self.stringArray_ch4.append(QtWidgets.QLabel("Channel 4"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Generator : DUMMY"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Brightness : 127"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Fade : 0"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Shutter : 0"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 1 : 89"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 2 : 54"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Effect 1 : DUMMY"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Effect 2 : DUMMY"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 3 : 110"))


        for item in self.stringArray_ch4:
            fi_ch4_CGL.addWidget(item)
#



        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.main_CL)

        # initialize threads
        self.midi_thread = threading.Thread(name='midi', target=midi)
        self.rendering_thread = threading.Thread(name='render', target=rendering)

        # what do we need the timer for? -> to execute functions periodically in the GUI e.g. updating Strings
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_fighter_values)
        timer.setInterval(20)
        timer.start()


        # start threads
        self.midi_thread.start()
        self.rendering_thread.start()

#    def start_download(self,info):
#        self.list_widget.addItem(info)

    def start_Renderer(self):
        """Routine to start all threads
        """
        global_parameter[0] = 1

    def stop_Renderer(self):
        global_parameter[0] = 0

    def update_fighter_values(self):
        self.stringArray_ch1[2].setText("Brightness : "+str(global_parameter[41]))
        self.stringArray_ch1[2].setText("Fade : "+str(global_parameter[42]))
        self.stringArray_ch1[2].setText("Shutter : "+str(global_parameter[43]))


'''
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
'''

def main():
    """main routine
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
