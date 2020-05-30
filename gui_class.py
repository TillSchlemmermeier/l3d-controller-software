import time
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
from labels import labels

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, array, label,parent=None):

        super(MainWindow, self).__init__()

        # get global arrays
        self.global_parameter = array
        self.global_label = label

        # initialize layout
        # creating main container-frame, parent it to QWindow
        self.main_CF = QtWidgets.QFrame(self)
        self.main_CF.setStyleSheet('background-color: rgba(50, 50, 50, 1)')
        self.setCentralWidget(self.main_CF)
        # creating layout and parent it to main container
        # is it correct, that main_CL now manages children of main_CF ?
        self.main_CL = QtWidgets.QHBoxLayout(self.main_CF)

        # creating the first subcontainer + layout, parenting it
        #control_CGF = QtWidgets.QFrame(self.main_CF)
        #self.main_CL.addWidget(control_CGF)
        #control_CGF.setStyleSheet('background-color: rgba(50, 50, 50, 1);')
        #control_CGL = QtWidgets.QVBoxLayout(control_CGF)
        #control_CGF.setFixedWidth(100)

        # Creatin subcontaiver for
        # creating the second subcontainer + layout, parenting it(LAUNCHPAD)

        self.padlabels = []
        for x in range(8):
            temp = []
            for y in range(8):
                label = QtWidgets.QLabel('init')
                label.setWordWrap(True)
                label.setStyleSheet("background-color: rgba("+str(x*10)+","+str(y*10)+", 0, 0.5);")
                temp.append(label)

            self.padlabels.append(temp)

        # define colors for different label layers
        self.colors = [[ '50', '50', '50', '1.0'], # closed
                       ['255',  '0',  '0', '0.8'], # channel 1 presets
                       ['255','165',  '0', '0.8'], # gen
                       ['255','255',  '0', '0.8'], # e 1
                       [  '0','255',  '0', '0.8'], # e 2
                       [  '0','255','255', '0.8'], # e 3
                       ['255',  '0',  '0', '0.8'], # channel 1
                       ['255','165',  '0', '0.8'], # gen
                       ['255','255',  '0', '0.8'], # e 1
                       [  '0','255',  '0', '0.8'], # e 2
                       [  '0','255','255', '0.8'], # e 3
                       ['255',  '0',  '0', '0.8'], # channel 1
                       ['255','165',  '0', '0.8'], # gen
                       ['255','255',  '0', '0.8'], # e 1
                       [  '0','255',  '0', '0.8'], # e 2
                       [  '0','255','255', '0.8'], # e 3
                       ['255',  '0',  '0', '0.8'], # channel 1
                       ['255','165',  '0', '0.8'], # gen
                       ['255','255',  '0', '0.8'], # e 1
                       [  '0','255',  '0', '0.8'], # e 2
                       [  '0','255','255', '0.8']] # e 3


        launchpad_CGF = QtWidgets.QFrame(self.main_CF)
        launchpad_CGF.setFixedWidth(683)
        self.main_CL.addWidget(launchpad_CGF)
        self.padlabels[x][y].setStyleSheet('background-color: rgba('+', '.join(self.colors[0])+');')

        launchpad_CGL = QtWidgets.QGridLayout(launchpad_CGF)

        for x in range(8):
            for y in range(8):
                launchpad_CGL.addWidget(self.padlabels[x][y],x,y)

        # doing the same with a third container(MIDIFIGHTER)
        fighter_CGF = QtWidgets.QFrame(self.main_CF)
        self.main_CL.addWidget(fighter_CGF)
        fighter_CGF.setStyleSheet('background-color: rgba(150, 150, 150, 1);')
        self.fighter_CGL = QtWidgets.QHBoxLayout(fighter_CGF)
        # SUB containers for fighter channels 1-4
        fi_ch1_CGF = QtWidgets.QFrame(fighter_CGF)
        fi_ch1_CGF.setFixedWidth(155)
        self.fighter_CGL.addWidget(fi_ch1_CGF)
        fi_ch1_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')
        fi_ch1_CGL = QtWidgets.QVBoxLayout(fi_ch1_CGF)

        fi_ch2_CGF = QtWidgets.QFrame(fighter_CGF)
        fi_ch2_CGF.setFixedWidth(155)
        self.fighter_CGL.addWidget(fi_ch2_CGF)
        fi_ch2_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')
        fi_ch2_CGL = QtWidgets.QVBoxLayout(fi_ch2_CGF)

        fi_ch3_CGF = QtWidgets.QFrame(fighter_CGF)
        fi_ch3_CGF.setFixedWidth(155)
        self.fighter_CGL.addWidget(fi_ch3_CGF)
        fi_ch3_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')
        fi_ch3_CGL = QtWidgets.QVBoxLayout(fi_ch3_CGF)

        fi_ch4_CGF = QtWidgets.QFrame(fighter_CGF)
        fi_ch4_CGF.setFixedWidth(155)
        self.fighter_CGL.addWidget(fi_ch4_CGF)
        fi_ch4_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')
        fi_ch4_CGL = QtWidgets.QVBoxLayout(fi_ch4_CGF)
####
        #self.button_StartR = QtWidgets.QPushButton("Start")
        #self.button_StopR = QtWidgets.QPushButton("Stop")
        #self.button_StartR.clicked.connect(self.start_Renderer)
        #self.button_StopR.clicked.connect(self.stop_Renderer)
        #self.string_GlobalBrightness = QtWidgets.QLabel("GB : ")

        #control_CGL.addWidget(self.button_StartR)
        #control_CGL.addWidget(self.button_StopR)
        #control_CGL.addWidget(self.string_GlobalBrightness)
###

        self.stringArray_ch1 = []
        self.stringArray_ch1.append(QtWidgets.QLabel("Channel 1"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Brightness : 127"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Fade : 0"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Shutter : 0"))
        self.stringArray_ch1.append(QtWidgets.QLabel("Generator: "))
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
            if "Generator" in item.text() or "Effect" in item.text():
                item.setStyleSheet("color: black; font: 18px; font-weight: bold");
            else:
                item.setStyleSheet("color: black; font: 14px;");
            fi_ch1_CGL.addWidget(item)
#
        self.stringArray_ch2 = []
        self.stringArray_ch2.append(QtWidgets.QLabel("Channel 2"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Brightness : 127"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Fade : 0"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Shutter : 0"))
        self.stringArray_ch2.append(QtWidgets.QLabel("Generator : DUMMY"))
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
            if "Generator" in item.text() or "Effect" in item.text():
                item.setStyleSheet("color: black; font: 18px; font-weight: bold");
            else:
                item.setStyleSheet("color: black; font: 14px;");
            fi_ch2_CGL.addWidget(item)
#
        self.stringArray_ch3 = []
        self.stringArray_ch3.append(QtWidgets.QLabel("Channel 3"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Brightness : 127"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Fade : 0"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Shutter : 0"))
        self.stringArray_ch3.append(QtWidgets.QLabel("Generator : DUMMY"))
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
            if "Generator" in item.text() or "Effect" in item.text():
                item.setStyleSheet("color: black; font: 18px; font-weight: bold");
            else:
                item.setStyleSheet("color: black; font: 14px;");
            fi_ch3_CGL.addWidget(item)
#
        self.stringArray_ch4 = []
        self.stringArray_ch4.append(QtWidgets.QLabel("Channel 4"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Brightness : 127"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Fade : 0"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Shutter : 0"))
        self.stringArray_ch4.append(QtWidgets.QLabel("Generator : DUMMY"))
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
            if "Generator" in item.text() or "Effect" in item.text():
                item.setStyleSheet("color: black; font: 18px; font-weight: bold");
            else:
                item.setStyleSheet("color: black; font: 14px;");
            fi_ch4_CGL.addWidget(item)

        #  copy params to check for changes
        # self.copied_params = deepcopy(global_parameter)
        self.copied_params = self.global_parameter[:]
        self.active_param = [-1, -1, -1, -1]

        # dict for converting global parameter to button
        self.conv_dict1 = {1:40, 2: 41, 3: 42, 4: 43,
                          5: 45, 6: 46, 7: 47,
                          8: 48, 10: 50,
                          11: 51, 12: 52, 13: 53,
                          15: 55, 16: 56,
                          17: 57, 18: 58,
                          20: 60, 21: 61, 22: 62,
                          23: 63}

        self.conv_dict2 = {1:70, 2: 71, 3: 72, 4: 73,
                          5: 75, 6: 76, 7: 77,
                          8: 78, 10: 80,
                          11: 81, 12: 82, 13: 83,
                          15: 85, 16: 86,
                          17: 87, 18: 88,
                          20: 90, 21: 91, 22: 92,
                          23: 93}
        self.conv_dict3 = {1: 100, 2: 101, 3: 102, 4: 103,
                          5: 105, 6: 106, 7: 107,
                          8: 108, 10: 110,
                          11: 111, 12: 112, 13: 113,
                          15: 115, 16: 116,
                          17: 117, 18: 118,
                          20: 120, 21: 121, 22: 122,
                          23: 123}

        self.conv_dict4 = {1: 130, 2: 131, 3: 132, 4: 133,
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
        #self.midi_thread = threading.Thread(name='midi_fighter', target=midi_fighter)
        #self.rendering_thread = threading.Thread(name='render', target=rendering)

        #global_parameter = mp.Array("d",[0,255])

        # what do we need the timer for? -> to execute functions periodically in the GUI e.g. updating Strings
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_fighter_values)
        #timer.timeout.connect(self.update_global_values)
        timer.timeout.connect(self.update_launchpad_values)
        timer.setInterval(10)
        timer.start()

        # start threads
        #self.midi_thread.start()


#    def start_download(self,info):
#        self.list_widget.addItem(info)

    def start_Renderer(self):
        """Routine to start all threads
        """
        self.global_parameter[0] = 1
        self.global_parameter[1] = 1
        self.global_parameter[2] = 0.0
        self.global_parameter[3] = 1.0
        self.global_parameter[20] = 1
        # activate channel 1
        self.global_parameter[40] = 1
        self.global_parameter[41] = 1
        # activate channel 2
        self.global_parameter[70] = 1

    def stop_Renderer(self):
        self.global_parameter[0] = 0

    #def update_global_values(self):
        #self.string_GlobalBrightness.setText("An : "+str(round(self.global_parameter[1],2)))

    def update_launchpad_values(self):

        # get labels of active menu
        # this is given by self.global_parameter[200]
        current_labels = labels[int(self.global_parameter[200]), :, :]

        # we need an index for the active generator/effect
        ind = -1
        # get current generator/effect
        if self.global_parameter[200] == 2:
            ind = self.global_parameter[20]
        elif self.global_parameter[200] == 3:
            ind = self.global_parameter[21]
        elif self.global_parameter[200] == 4:
            ind = self.global_parameter[22]
        elif self.global_parameter[200] == 5:
            ind = self.global_parameter[23]

        if self.global_parameter[200] == 7:
            ind = self.global_parameter[25]
        elif self.global_parameter[200] == 8:
            ind = self.global_parameter[26]
        elif self.global_parameter[200] == 9:
            ind = self.global_parameter[27]
        elif self.global_parameter[200] == 10:
            ind = self.global_parameter[28]

        if self.global_parameter[200] == 12:
            ind = self.global_parameter[30]
        elif self.global_parameter[200] == 13:
            ind = self.global_parameter[31]
        elif self.global_parameter[200] == 14:
            ind = self.global_parameter[32]
        elif self.global_parameter[200] == 15:
            ind = self.global_parameter[33]

        if self.global_parameter[200] == 17:
            ind = self.global_parameter[35]
        elif self.global_parameter[200] == 18:
            ind = self.global_parameter[36]
        elif self.global_parameter[200] == 19:
            ind = self.global_parameter[37]
        elif self.global_parameter[200] == 20:
            ind = self.global_parameter[38]

        counter = 0
        # loop over elements in pad panel
        for x in range(8):
            for y in range(8):
                # add text labels
                self.padlabels[x][y].setText(current_labels[x, y])
                self.padlabels[x][y].setAlignment(QtCore.Qt.AlignCenter)
                # self.padlabels[x][y].setWordWrap(True)
                # get color - don't do a shallow copy here!
                color = self.colors[int(self.global_parameter[200])][:]

                if x in [2, 5] or y in [2, 5]:
                    for i in range(3):
                        color[i] = str(np.clip(int(color[i]) - 50, 0, 255))


                if counter == ind + 1:
                    # active generator/effect gets red border
                    self.padlabels[x][y].setStyleSheet('Background-color: rgba('+', '.join(color)+'); color: red; border-style: dashed; border-width: 4px; border-color: red; text-align: center;')
                else:
                    self.padlabels[x][y].setStyleSheet('background-color: rgba('+', '.join(color)+'); text-align: center;')

                counter+=1


    def update_fighter_values(self):
        self.stringArray_ch1[1].setText("Brightness : "+str(round(self.global_parameter[41],2)))
        self.stringArray_ch1[2].setText("Fade : "+str(round(self.global_parameter[42],2)))
        self.stringArray_ch1[3].setText("Shutter : "+str(round(self.global_parameter[43],2)))
        self.stringArray_ch1[4].setText("G: "+str(self.global_label[0],'utf-8'))
        self.stringArray_ch1[5].setText(str(self.global_label[1],'utf-8')+" : "+str(round(self.global_parameter[45],2)))
        self.stringArray_ch1[6].setText(str(self.global_label[2],'utf-8')+" : "+str(round(self.global_parameter[46],2)))
        self.stringArray_ch1[7].setText(str(self.global_label[3],'utf-8')+" : "+str(round(self.global_parameter[47],2)))
        self.stringArray_ch1[8].setText(str(self.global_label[4],'utf-8')+" : "+str(round(self.global_parameter[48],2)))
        self.stringArray_ch1[9].setText("E: "+str(self.global_label[5],'utf-8'))
        self.stringArray_ch1[10].setText(str(self.global_label[6],'utf-8')+" : "+str(round(self.global_parameter[50],2)))
        self.stringArray_ch1[11].setText(str(self.global_label[7],'utf-8')+" : "+str(round(self.global_parameter[51],2)))
        self.stringArray_ch1[12].setText(str(self.global_label[8],'utf-8')+" : "+str(round(self.global_parameter[52],2)))
        self.stringArray_ch1[13].setText(str(self.global_label[9],'utf-8')+" : "+str(round(self.global_parameter[53],2)))
        self.stringArray_ch1[14].setText("E: "+str(self.global_label[10],'utf-8'))
        self.stringArray_ch1[15].setText(str(self.global_label[11],'utf-8')+" : "+str(round(self.global_parameter[55],2)))
        self.stringArray_ch1[16].setText(str(self.global_label[12],'utf-8')+" : "+str(round(self.global_parameter[56],2)))
        self.stringArray_ch1[17].setText(str(self.global_label[13],'utf-8')+" : "+str(round(self.global_parameter[57],2)))
        self.stringArray_ch1[18].setText(str(self.global_label[14],'utf-8')+" : "+str(round(self.global_parameter[58],2)))
        self.stringArray_ch1[19].setText("E: "+str(self.global_label[15],'utf-8'))
        self.stringArray_ch1[20].setText(str(self.global_label[16],'utf-8')+" : "+str(round(self.global_parameter[60],2)))
        self.stringArray_ch1[21].setText(str(self.global_label[17],'utf-8')+" : "+str(round(self.global_parameter[61],2)))
        self.stringArray_ch1[22].setText(str(self.global_label[18],'utf-8')+" : "+str(round(self.global_parameter[62],2)))
        self.stringArray_ch1[23].setText(str(self.global_label[19],'utf-8')+" : "+str(round(self.global_parameter[63],2)))


        self.stringArray_ch2[1].setText("Brightness : "+str(round(self.global_parameter[71],2)))
        self.stringArray_ch2[2].setText("Fade : "+str(round(self.global_parameter[72],2)))
        self.stringArray_ch2[3].setText("Shutter : "+str(round(self.global_parameter[73],2)))
        self.stringArray_ch2[4].setText("G: "+str(self.global_label[20],'utf-8'))
        self.stringArray_ch2[5].setText(str(self.global_label[21],'utf-8')+" : "+str(round(self.global_parameter[75],2)))
        self.stringArray_ch2[6].setText(str(self.global_label[22],'utf-8')+" : "+str(round(self.global_parameter[76],2)))
        self.stringArray_ch2[7].setText(str(self.global_label[23],'utf-8')+" : "+str(round(self.global_parameter[77],2)))
        self.stringArray_ch2[8].setText(str(self.global_label[24],'utf-8')+" : "+str(round(self.global_parameter[78],2)))
        self.stringArray_ch2[9].setText("E: "+str(self.global_label[25],'utf-8'))
        self.stringArray_ch2[10].setText(str(self.global_label[26],'utf-8')+" : "+str(round(self.global_parameter[80],2)))
        self.stringArray_ch2[11].setText(str(self.global_label[27],'utf-8')+" : "+str(round(self.global_parameter[81],2)))
        self.stringArray_ch2[12].setText(str(self.global_label[28],'utf-8')+" : "+str(round(self.global_parameter[82],2)))
        self.stringArray_ch2[13].setText(str(self.global_label[29],'utf-8')+" : "+str(round(self.global_parameter[83],2)))
        self.stringArray_ch2[14].setText("E: "+str(self.global_label[30],'utf-8'))
        self.stringArray_ch2[15].setText(str(self.global_label[31],'utf-8')+" : "+str(round(self.global_parameter[85],2)))
        self.stringArray_ch2[16].setText(str(self.global_label[32],'utf-8')+" : "+str(round(self.global_parameter[86],2)))
        self.stringArray_ch2[17].setText(str(self.global_label[33],'utf-8')+" : "+str(round(self.global_parameter[87],2)))
        self.stringArray_ch2[18].setText(str(self.global_label[34],'utf-8')+" : "+str(round(self.global_parameter[88],2)))
        self.stringArray_ch2[19].setText("E: "+str(self.global_label[35],'utf-8'))
        self.stringArray_ch2[20].setText(str(self.global_label[36],'utf-8')+" : "+str(round(self.global_parameter[90],2)))
        self.stringArray_ch2[21].setText(str(self.global_label[37],'utf-8')+" : "+str(round(self.global_parameter[91],2)))
        self.stringArray_ch2[22].setText(str(self.global_label[38],'utf-8')+" : "+str(round(self.global_parameter[92],2)))
        self.stringArray_ch2[23].setText(str(self.global_label[39],'utf-8')+" : "+str(round(self.global_parameter[93],2)))


        self.stringArray_ch3[1].setText("Brightness : "+str(round(self.global_parameter[101],2)))
        self.stringArray_ch3[2].setText("Fade : "+str(round(self.global_parameter[102],2)))
        self.stringArray_ch3[3].setText("Shutter : "+str(round(self.global_parameter[103],2)))
        self.stringArray_ch3[4].setText("G: "+str(self.global_label[40],'utf-8'))
        self.stringArray_ch3[5].setText(str(self.global_label[41],'utf-8')+" : "+str(round(self.global_parameter[105],2)))
        self.stringArray_ch3[6].setText(str(self.global_label[42],'utf-8')+" : "+str(round(self.global_parameter[106],2)))
        self.stringArray_ch3[7].setText(str(self.global_label[43],'utf-8')+" : "+str(round(self.global_parameter[107],2)))
        self.stringArray_ch3[8].setText(str(self.global_label[44],'utf-8')+" : "+str(round(self.global_parameter[108],2)))
        self.stringArray_ch3[9].setText("E: "+str(self.global_label[45],'utf-8'))
        self.stringArray_ch3[10].setText(str(self.global_label[46],'utf-8')+" : "+str(round(self.global_parameter[110],2)))
        self.stringArray_ch3[11].setText(str(self.global_label[47],'utf-8')+" : "+str(round(self.global_parameter[111],2)))
        self.stringArray_ch3[12].setText(str(self.global_label[48],'utf-8')+" : "+str(round(self.global_parameter[112],2)))
        self.stringArray_ch3[13].setText(str(self.global_label[49],'utf-8')+" : "+str(round(self.global_parameter[113],2)))
        self.stringArray_ch3[14].setText("E: "+str(self.global_label[50],'utf-8'))
        self.stringArray_ch3[15].setText(str(self.global_label[51],'utf-8')+" : "+str(round(self.global_parameter[115],2)))
        self.stringArray_ch3[16].setText(str(self.global_label[52],'utf-8')+" : "+str(round(self.global_parameter[116],2)))
        self.stringArray_ch3[17].setText(str(self.global_label[53],'utf-8')+" : "+str(round(self.global_parameter[117],2)))
        self.stringArray_ch3[18].setText(str(self.global_label[54],'utf-8')+" : "+str(round(self.global_parameter[118],2)))
        self.stringArray_ch3[19].setText("E: "+str(self.global_label[55],'utf-8'))
        self.stringArray_ch3[20].setText(str(self.global_label[56],'utf-8')+" : "+str(round(self.global_parameter[120],2)))
        self.stringArray_ch3[21].setText(str(self.global_label[57],'utf-8')+" : "+str(round(self.global_parameter[121],2)))
        self.stringArray_ch3[22].setText(str(self.global_label[58],'utf-8')+" : "+str(round(self.global_parameter[122],2)))
        self.stringArray_ch3[23].setText(str(self.global_label[59],'utf-8')+" : "+str(round(self.global_parameter[123],2)))


        self.stringArray_ch4[1].setText("Brightness : "+str(round(self.global_parameter[131],2)))
        self.stringArray_ch4[2].setText("Fade : "+str(round(self.global_parameter[132],2)))
        self.stringArray_ch4[3].setText("Shutter : "+str(round(self.global_parameter[133],2)))
        self.stringArray_ch4[4].setText("G: "+str(self.global_label[60],'utf-8'))
        self.stringArray_ch4[5].setText(str(self.global_label[61],'utf-8')+" : "+str(round(self.global_parameter[135],2)))
        self.stringArray_ch4[6].setText(str(self.global_label[62],'utf-8')+" : "+str(round(self.global_parameter[136],2)))
        self.stringArray_ch4[7].setText(str(self.global_label[63],'utf-8')+" : "+str(round(self.global_parameter[137],2)))
        self.stringArray_ch4[8].setText(str(self.global_label[64],'utf-8')+" : "+str(round(self.global_parameter[138],2)))
        self.stringArray_ch4[9].setText("E: "+str(self.global_label[65],'utf-8'))
        self.stringArray_ch4[10].setText(str(self.global_label[66],'utf-8')+" : "+str(round(self.global_parameter[140],2)))
        self.stringArray_ch4[11].setText(str(self.global_label[67],'utf-8')+" : "+str(round(self.global_parameter[141],2)))
        self.stringArray_ch4[12].setText(str(self.global_label[68],'utf-8')+" : "+str(round(self.global_parameter[142],2)))
        self.stringArray_ch4[13].setText(str(self.global_label[69],'utf-8')+" : "+str(round(self.global_parameter[143],2)))
        self.stringArray_ch4[14].setText("E: "+str(self.global_label[70],'utf-8'))
        self.stringArray_ch4[15].setText(str(self.global_label[71],'utf-8')+" : "+str(round(self.global_parameter[145],2)))
        self.stringArray_ch4[16].setText(str(self.global_label[72],'utf-8')+" : "+str(round(self.global_parameter[146],2)))
        self.stringArray_ch4[17].setText(str(self.global_label[73],'utf-8')+" : "+str(round(self.global_parameter[147],2)))
        self.stringArray_ch4[18].setText(str(self.global_label[74],'utf-8')+" : "+str(round(self.global_parameter[148],2)))
        self.stringArray_ch4[19].setText("E: "+str(self.global_label[75],'utf-8'))
        self.stringArray_ch4[20].setText(str(self.global_label[76],'utf-8')+" : "+str(round(self.global_parameter[150],2)))
        self.stringArray_ch4[21].setText(str(self.global_label[77],'utf-8')+" : "+str(round(self.global_parameter[151],2)))
        self.stringArray_ch4[22].setText(str(self.global_label[78],'utf-8')+" : "+str(round(self.global_parameter[152],2)))
        self.stringArray_ch4[23].setText(str(self.global_label[79],'utf-8')+" : "+str(round(self.global_parameter[153],2)))

        # check for last changed value
        index_changed = np.where((np.array(self.copied_params) == np.array(self.global_parameter)) == False)[0]

        if np.shape(index_changed)[0] > 1:
            index_changed = index_changed[0]

        # lets just  do it for the first channel
        for item_1, item_2, item_3, item_4 in zip(self.conv_dict1.items(), self.conv_dict2.items(), self.conv_dict3.items(), self.conv_dict4.items()):
            # compare value with last changed key
            if item_1[1] == index_changed:
                # save key of last changed value:question
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
                if "G:" in item.text() or "E:" in item.text():
                    item.setStyleSheet("color: black; font: 18px;font-weight: bold");
                else:
                    item.setStyleSheet("color: black; font: 18px;");

        if index_changed in range(70,94):
            for item in self.stringArray_ch2:
                if "G:" in item.text() or "E:" in item.text():
                    item.setStyleSheet("color: black; font: 18px;font-weight: bold");
                else:
                    item.setStyleSheet("color: black; font: 18px;");

        if index_changed in range(100,124):
            for item in self.stringArray_ch3:
                if "G:" in item.text() or "E:" in item.text():
                    item.setStyleSheet("color: black; font: 18px;font-weight: bold");
                else:
                    item.setStyleSheet("color: black; font: 18px;");

        if index_changed in range(130,154):
            for item in self.stringArray_ch4:
                if "G:" in item.text() or "E:" in item.text():
                    item.setStyleSheet("color: black; font: 18px;font-weight: bold");
                else:
                    item.setStyleSheet("color: black; font: 18px;");

        # colors for each area
        oncolor = ['#ffa500', '#ffff00', '#00cc00', '#00dcff']
        offcolor = ['#ffe4b2', '#ffffb2', '#b2efb2', '#b2f4ff']

        # areas for generators, effect1, ...
        area = [[ 5, 6, 7, 8],
                [10,11,12,13],
                [15,16,17,18],
                [20,21,22,23]]
        # loop through all fields and set colors

        if self.active_param != -1:
            for ar,onc,offc in zip(area,oncolor,offcolor):
                if self.active_param[0] in ar:
                    for a in ar:
                        if index_changed in range(40,64):
                            self.stringArray_ch1[a].setStyleSheet("color: black; font: 20px; background-color: "+onc)
                else:
                    for a in ar:
                        if index_changed in range(40,64):
                            self.stringArray_ch1[a].setStyleSheet("color: black; font: 20px; background-color: "+offc)

                if self.active_param[1] in ar:
                    for a in ar:
                        if index_changed in range(70,94):
                            self.stringArray_ch2[a].setStyleSheet("color: black; font: 20px; background-color: "+onc)
                else:
                    for a in ar:
                        if index_changed in range(70,94):
                            self.stringArray_ch2[a].setStyleSheet("color: black; font: 20px; background-color: "+offc)

                if self.active_param[2] in ar:
                    for a in ar:
                        if index_changed in range(100,124):
                            self.stringArray_ch3[a].setStyleSheet("color: black; font: 20px; background-color: "+onc)
                else:
                    for a in ar:
                        if index_changed in range(100,124):
                            self.stringArray_ch3[a].setStyleSheet("color: black; font: 20px; background-color: "+offc)

                if self.active_param[3] in ar:
                    for a in ar:
                        if index_changed in range(130,154):
                            self.stringArray_ch4[a].setStyleSheet("color: black; font: 20px; background-color: "+onc)
                else:
                    for a in ar:
                        if index_changed in range(130,154):
                            self.stringArray_ch4[a].setStyleSheet("color: black; font: 20px; background-color: "+offc)

        self.copied_params = self.global_parameter[:]
