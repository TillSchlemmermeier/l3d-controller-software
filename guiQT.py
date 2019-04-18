##!/usr/bin/python3
import threading    # do we need this or is QT taking care of everything?
import time
# import rendering class
from rendering_engine import rendering_engine
# import global variable
from global_parameter_module import global_parameter
from copy import deepcopy
import sys
import tempfile     # what is this?
import subprocess   # obsolete?
#import urllib.request
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np


from MidiDevice import class_fighter, class_akai
#from PyQt5.QtCore import QObject,QThread, pyqtSigna
#from mainwindow import Ui_MainWindow


def midi_fighter():
    '''
    Midi Thread
    '''
    print('...starting midi thread')
    # we should do something to detect ports! -> YES we should :)
    midifighter = class_fighter(in_port = 2,out_port = 2)
    launchpad = class_akai()

def midi_akai():
    '''
    Midi Thread
    '''
    print('...starting midi thread')
    # we should do something to detect ports! -> YES we should :)
    midifighter = class_fighter(in_port = 2,out_port = 2)
    launchpad = class_akai()


def rendering(pause_time = 0.001, log = False):
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

        # creating the second subcontainer + layout, parenting it(LAUNCHPAD)
        launchpad_CGF = QtWidgets.QFrame(self.main_CF)
        self.main_CL.addWidget(launchpad_CGF)
        launchpad_CGF.setStyleSheet('background-color: rgba(0, 150, 0, 1);')
        launchpad_CGL = QtWidgets.QHBoxLayout(launchpad_CGF)
        # SUB containers for launchpad columns 1-8
        la_co1_CGF = QtWidgets.QFrame(launchpad_CGF)
        launchpad_CGL.addWidget(la_co1_CGF)
        la_co1_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        la_co1_CGL = QtWidgets.QVBoxLayout(la_co1_CGF)

        la_co2_CGF = QtWidgets.QFrame(launchpad_CGF)
        launchpad_CGL.addWidget(la_co2_CGF)
        la_co2_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        la_co2_CGL = QtWidgets.QVBoxLayout(la_co2_CGF)

        la_co3_CGF = QtWidgets.QFrame(launchpad_CGF)
        launchpad_CGL.addWidget(la_co3_CGF)
        la_co3_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        la_co3_CGL = QtWidgets.QVBoxLayout(la_co3_CGF)

        la_co4_CGF = QtWidgets.QFrame(launchpad_CGF)
        launchpad_CGL.addWidget(la_co4_CGF)
        la_co4_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        la_co4_CGL = QtWidgets.QVBoxLayout(la_co4_CGF)

        la_co5_CGF = QtWidgets.QFrame(launchpad_CGF)
        launchpad_CGL.addWidget(la_co5_CGF)
        la_co5_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        la_co5_CGL = QtWidgets.QVBoxLayout(la_co5_CGF)

        la_co6_CGF = QtWidgets.QFrame(launchpad_CGF)
        launchpad_CGL.addWidget(la_co6_CGF)
        la_co6_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        la_co6_CGL = QtWidgets.QVBoxLayout(la_co6_CGF)

        la_co7_CGF = QtWidgets.QFrame(launchpad_CGF)
        launchpad_CGL.addWidget(la_co7_CGF)
        la_co7_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        la_co7_CGL = QtWidgets.QVBoxLayout(la_co7_CGF)

        la_co8_CGF = QtWidgets.QFrame(launchpad_CGF)
        launchpad_CGL.addWidget(la_co8_CGF)
        la_co8_CGF.setStyleSheet('background-color: rgba(200, 200, 200, 1);')
        la_co8_CGL = QtWidgets.QVBoxLayout(la_co8_CGF)



        # doing the same with a third container(MIDIFIGHTER)
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
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Effect 1 : DUMMY"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Effect 2 : DUMMY"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Effect 3 : DUMMY"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Parameter 4 : 110"))


        for item in self.stringArray_ch1:
            item.setStyleSheet("color: black; font: 9px;");
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
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Effect 1 : DUMMY"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Effect 2 : DUMMY"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Effect 3 : DUMMY"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Parameter 4 : 110"))



        for item in self.stringArray_ch2:
            item.setStyleSheet("color: black; font: 9px;");
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
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Effect 1 : DUMMY"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Effect 2 : DUMMY"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Effect 3: DUMMY"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Parameter 4 : 110"))

        for item in self.stringArray_ch3:
            item.setStyleSheet("color: black; font: 9px;");
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
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Effect 1 : DUMMY"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Effect 2 : DUMMY"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 4 : 110"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Effect 3 : DUMMY"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 1 : 0"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 2 : 127"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 3 : 110"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Parameter 4 : 110"))

        for item in self.stringArray_ch4:
            item.setStyleSheet("color: black; font: 9px;");
            fi_ch4_CGL.addWidget(item)

        #  copy params to check for changes
        self.copied_params = deepcopy(global_parameter)
        self.active_param = [-1, -1, -1, -1]

        # dict for converting global parameter to button
        self.conv_dict1 = {2: 41, 3: 42, 4: 43,
                          5: 45, 6: 46, 7: 47,
                          8: 48, 10: 50,
                          11: 51, 12: 52, 13: 53,
                          15: 55, 16: 56,
                          17: 57, 18: 58,
                          20: 60, 21: 61, 22: 62,
                          23: 63}

        self.conv_dict2 = {2: 71, 3: 72, 4: 73,
                          5: 75, 6: 76, 7: 77,
                          8: 78, 10: 80,
                          11: 81, 12: 82, 13: 83,
                          15: 85, 16: 86,
                          17: 87, 18: 88,
                          20: 90, 21: 91, 22: 92,
                          23: 93}
        self.conv_dict3 = {2: 101, 3: 102, 4: 103,
                          5: 105, 6: 106, 7: 107,
                          8: 108, 10: 110,
                          11: 111, 12: 112, 13: 113,
                          15: 115, 16: 116,
                          17: 117, 18: 118,
                          20: 120, 21: 121, 22: 122,
                          23: 123}

        self.conv_dict4 = {2: 131, 3: 132, 4: 133,
                          5: 135, 6: 136, 7: 137,
                          8: 138, 10: 140,
                          11: 141, 12: 142, 13: 143,
                          15: 145, 16: 146,
                          17: 147, 18: 148,
                          20: 150, 21: 151, 22: 152,
                          23: 153}

        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.main_CL)

        # initialize threads
        self.midi_thread = threading.Thread(name='midi_fighter', target=midi_fighter)
        self.rendering_thread = threading.Thread(name='render', target=rendering)

        # what do we need the timer for? -> to execute functions periodically in the GUI e.g. updating Strings
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_fighter_values)
        timer.setInterval(0.1)
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
        global_parameter[1] = 1
        global_parameter[2] = 0.5
        global_parameter[3] = 1.0
        global_parameter[20] = 1
        global_parameter[40] = 1
        global_parameter[41] = 1


    def stop_Renderer(self):
        global_parameter[0] = 0

    def update_fighter_values(self):
        self.stringArray_ch1[2].setText("Brightness : "+str(round(global_parameter[41],2)))
        self.stringArray_ch1[3].setText("Fade : "+str(round(global_parameter[42],2)))
        self.stringArray_ch1[4].setText("Shutter : "+str(round(global_parameter[43],2)))
        self.stringArray_ch1[5].setText("Parameter 1 : "+str(round(global_parameter[45],2)))
        self.stringArray_ch1[6].setText("Parameter 2 : "+str(round(global_parameter[46],2)))
        self.stringArray_ch1[7].setText("Parameter 3 : "+str(round(global_parameter[47],2)))
        self.stringArray_ch1[8].setText("Parameter 4 : "+str(round(global_parameter[48],2)))
        self.stringArray_ch1[10].setText("Parameter 1 : "+str(round(global_parameter[50],2)))
        self.stringArray_ch1[11].setText("Parameter 2 : "+str(round(global_parameter[51],2)))
        self.stringArray_ch1[12].setText("Parameter 3 : "+str(round(global_parameter[52],2)))
        self.stringArray_ch1[13].setText("Parameter 4 : "+str(round(global_parameter[53],2)))
        self.stringArray_ch1[15].setText("Parameter 1 : "+str(round(global_parameter[55],2)))
        self.stringArray_ch1[16].setText("Parameter 2 : "+str(round(global_parameter[56],2)))
        self.stringArray_ch1[17].setText("Parameter 3 : "+str(round(global_parameter[57],2)))
        self.stringArray_ch1[18].setText("Parameter 4 : "+str(round(global_parameter[58],2)))
        self.stringArray_ch1[20].setText("Parameter 1 : "+str(round(global_parameter[60],2)))
        self.stringArray_ch1[21].setText("Parameter 2 : "+str(round(global_parameter[61],2)))
        self.stringArray_ch1[22].setText("Parameter 3 : "+str(round(global_parameter[62],2)))
        self.stringArray_ch1[23].setText("Parameter 4 : "+str(round(global_parameter[63],2)))

        self.stringArray_ch2[2].setText("Brightness : "+str(round(global_parameter[71],2)))
        self.stringArray_ch2[3].setText("Fade : "+str(round(global_parameter[72],2)))
        self.stringArray_ch2[4].setText("Shutter : "+str(round(global_parameter[73],2)))
        self.stringArray_ch2[5].setText("Parameter 1 : "+str(round(global_parameter[75],2)))
        self.stringArray_ch2[6].setText("Parameter 2 : "+str(round(global_parameter[76],2)))
        self.stringArray_ch2[7].setText("Parameter 3 : "+str(round(global_parameter[77],2)))
        self.stringArray_ch2[8].setText("Parameter 4 : "+str(round(global_parameter[78],2)))
        self.stringArray_ch2[10].setText("Parameter 1 : "+str(round(global_parameter[80],2)))
        self.stringArray_ch2[11].setText("Parameter 2 : "+str(round(global_parameter[81],2)))
        self.stringArray_ch2[12].setText("Parameter 3 : "+str(round(global_parameter[82],2)))
        self.stringArray_ch2[13].setText("Parameter 4 : "+str(round(global_parameter[83],2)))
        self.stringArray_ch2[15].setText("Parameter 1 : "+str(round(global_parameter[85],2)))
        self.stringArray_ch2[16].setText("Parameter 2 : "+str(round(global_parameter[86],2)))
        self.stringArray_ch2[17].setText("Parameter 3 : "+str(round(global_parameter[87],2)))
        self.stringArray_ch2[18].setText("Parameter 4 : "+str(round(global_parameter[88],2)))
        self.stringArray_ch2[20].setText("Parameter 1 : "+str(round(global_parameter[90],2)))
        self.stringArray_ch2[21].setText("Parameter 2 : "+str(round(global_parameter[91],2)))
        self.stringArray_ch2[22].setText("Parameter 3 : "+str(round(global_parameter[92],2)))
        self.stringArray_ch2[23].setText("Parameter 4 : "+str(round(global_parameter[93],2)))

        self.stringArray_ch3[2].setText("Brightness : "+str(round(global_parameter[101],2)))
        self.stringArray_ch3[3].setText("Fade : "+str(round(global_parameter[102],2)))
        self.stringArray_ch3[4].setText("Shutter : "+str(round(global_parameter[103],2)))
        self.stringArray_ch3[5].setText("Parameter 1 : "+str(round(global_parameter[105],2)))
        self.stringArray_ch3[6].setText("Parameter 2 : "+str(round(global_parameter[106],2)))
        self.stringArray_ch3[7].setText("Parameter 3 : "+str(round(global_parameter[107],2)))
        self.stringArray_ch3[8].setText("Parameter 4 : "+str(round(global_parameter[108],2)))
        self.stringArray_ch3[10].setText("Parameter 1 : "+str(round(global_parameter[110],2)))
        self.stringArray_ch3[11].setText("Parameter 2 : "+str(round(global_parameter[111],2)))
        self.stringArray_ch3[12].setText("Parameter 3 : "+str(round(global_parameter[112],2)))
        self.stringArray_ch3[13].setText("Parameter 4 : "+str(round(global_parameter[113],2)))
        self.stringArray_ch3[15].setText("Parameter 1 : "+str(round(global_parameter[115],2)))
        self.stringArray_ch3[16].setText("Parameter 2 : "+str(round(global_parameter[116],2)))
        self.stringArray_ch3[17].setText("Parameter 3 : "+str(round(global_parameter[117],2)))
        self.stringArray_ch3[18].setText("Parameter 4 : "+str(round(global_parameter[118],2)))
        self.stringArray_ch3[20].setText("Parameter 1 : "+str(round(global_parameter[120],2)))
        self.stringArray_ch3[21].setText("Parameter 2 : "+str(round(global_parameter[121],2)))
        self.stringArray_ch3[22].setText("Parameter 3 : "+str(round(global_parameter[122],2)))
        self.stringArray_ch3[23].setText("Parameter 4 : "+str(round(global_parameter[123],2)))

        self.stringArray_ch4[2].setText("Brightness : "+str(round(global_parameter[131],2)))
        self.stringArray_ch4[3].setText("Fade : "+str(round(global_parameter[132],2)))
        self.stringArray_ch4[4].setText("Shutter : "+str(round(global_parameter[133],2)))
        self.stringArray_ch4[5].setText("Parameter 1 : "+str(round(global_parameter[135],2)))
        self.stringArray_ch4[6].setText("Parameter 2 : "+str(round(global_parameter[136],2)))
        self.stringArray_ch4[7].setText("Parameter 3 : "+str(round(global_parameter[137],2)))
        self.stringArray_ch4[8].setText("Parameter 4 : "+str(round(global_parameter[138],2)))
        self.stringArray_ch4[10].setText("Parameter 1 : "+str(round(global_parameter[140],2)))
        self.stringArray_ch4[11].setText("Parameter 2 : "+str(round(global_parameter[141],2)))
        self.stringArray_ch4[12].setText("Parameter 3 : "+str(round(global_parameter[142],2)))
        self.stringArray_ch4[13].setText("Parameter 4 : "+str(round(global_parameter[143],2)))
        self.stringArray_ch4[15].setText("Parameter 1 : "+str(round(global_parameter[145],2)))
        self.stringArray_ch4[16].setText("Parameter 2 : "+str(round(global_parameter[146],2)))
        self.stringArray_ch4[17].setText("Parameter 3 : "+str(round(global_parameter[147],2)))
        self.stringArray_ch4[18].setText("Parameter 4 : "+str(round(global_parameter[148],2)))
        self.stringArray_ch4[20].setText("Parameter 1 : "+str(round(global_parameter[150],2)))
        self.stringArray_ch4[21].setText("Parameter 2 : "+str(round(global_parameter[151],2)))
        self.stringArray_ch4[22].setText("Parameter 3 : "+str(round(global_parameter[152],2)))
        self.stringArray_ch4[23].setText("Parameter 4 : "+str(round(global_parameter[153],2)))

        # check for last changed value
        index_changed = np.where((self.copied_params == global_parameter) == False)[0]

        if np.shape(index_changed)[0] > 1:
            index_changed = index_changed[0]

#        print(np.where((self.copied_params == global_parameter) == False)[0])

        # lets just  do it for the first channel
        for item_1, item_2, item_3, item_4 in zip(self.conv_dict1.items(), self.conv_dict2.items(), self.conv_dict3.items(), self.conv_dict4.items()):
            # compare value with last changed key
            if item_1[1] == index_changed:
                # save key of last changed value
                self.active_param[0] = item_1[0]

            if item_2[1] == index_changed:
                self.active_param[1] = item_2[0]

            if item_3[1] == index_changed:
                self.active_param[2] = item_3[0]

            if item_4[1] == index_changed:
                self.active_param[3] = item_4[0]

        # write all back to normal

        if index_changed in range(40,64):
            for item in self.stringArray_ch1:
                item.setStyleSheet("color: black; font: 9px;")

        if index_changed in range(70,94):
            for item in self.stringArray_ch2:
                item.setStyleSheet("color: black; font: 9px;")

        if index_changed in range(100,124):
            for item in self.stringArray_ch3:
                item.setStyleSheet("color: black; font: 9px;")

        if index_changed in range(130,154):
            for item in self.stringArray_ch4:
                item.setStyleSheet("color: black; font: 9px;")

        # colors for each area
        color = ['#0066cc', '#00cc00', '#ff9933', '#ff0066']

        # areas for generators, effect1, ...
        area = [[ 5, 6, 7, 8],
                [10,11,12,13],
                [15,16,17,18],
                [20,21,22,23]]
        # loop through all fields and set colors

        if self.active_param != -1:
            for ar,c in zip(area,color):
                if self.active_param[0] in ar:
                    for a in ar:
                        if index_changed in range(40,64):
                            self.stringArray_ch1[a].setStyleSheet("color: black; font: 15px; background-color: "+c)

                if self.active_param[1] in ar:
                    for a in ar:
                        if index_changed in range(70,94):
                            self.stringArray_ch2[a].setStyleSheet("color: black; font: 15px; background-color: "+c)

                if self.active_param[2] in ar:
                    for a in ar:
                        if index_changed in range(100,124):
                            self.stringArray_ch3[a].setStyleSheet("color: black; font: 15px; background-color: "+c)

                if self.active_param[3] in ar:
                    for a in ar:
                        if index_changed in range(130,154):
                            self.stringArray_ch4[a].setStyleSheet("color: black; font: 15px; background-color: "+c)

#                        self.stringArray_ch2[a].setStyleSheet("color: black; font: 12px; background-color: "+c)
#                        self.stringArray_ch3[a].setStyleSheet("color: black; font: 12px; background-color: "+c)
#                        self.stringArray_ch4[a].setStyleSheet("color: black; font: 12px; background-color: "+c)
                #self.stringArray_ch1[6].setStyleSheet("color: black; font: 12px; background-color: blue")
                #self.stringArray_ch1[7].setStyleSheet("color: black; font: 12px; background-color: blue")
                #self.stringArray_ch1[8].setStyleSheet("color: black; font: 12px; background-color: blue")
            '''
            if(self.active_param in (10,11,12,13)):
                self.stringArray_ch1[10].setStyleSheet("color: black; font: 12px; background-color: green")
                self.stringArray_ch1[11].setStyleSheet("color: black; font: 12px; background-color: green")
                self.stringArray_ch1[12].setStyleSheet("color: black; font: 12px; background-color: green")
                self.stringArray_ch1[13].setStyleSheet("color: black; font: 12px; background-color: green")
            if(self.active_param in (15,16,17,18)):
                self.stringArray_ch1[15].setStyleSheet("color: black; font: 12px; background-color: orange")
                self.stringArray_ch1[16].setStyleSheet("color: black; font: 12px; background-color: orange")
                self.stringArray_ch1[17].setStyleSheet("color: black; font: 12px; background-color: orange")
                self.stringArray_ch1[18].setStyleSheet("color: black; font: 12px; background-color: orange")
            if(self.active_param in (20,21,22,23)):
                self.stringArray_ch1[20].setStyleSheet("color: black; font: 12px; background-color: pink")
                self.stringArray_ch1[21].setStyleSheet("color: black; font: 12px; background-color: pink")
                self.stringArray_ch1[22].setStyleSheet("color: black; font: 12px; background-color: pink")
                self.stringArray_ch1[23].setStyleSheet("color: black; font: 12px; background-color: pink")
            '''
        #for item in self.stringArray_ch4:
        #    item.setStyleSheet("color: black; font: 9px;");

        self.copied_params = deepcopy(global_parameter)




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
