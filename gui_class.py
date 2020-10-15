import time
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
from labels import labels
from multiprocessing import shared_memory

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, array, label ,parent=None):

        super(MainWindow, self).__init__()

        # get global arrays
        self.global_parameter = array
        self.global_label = label
        self.shared_mem_gui_vals = shared_memory.SharedMemory(name = "GuiValues1")


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
        self.fi_ch1_CGF = QtWidgets.QFrame(fighter_CGF)
        self.fi_ch1_CGF.setFixedWidth(155)
        self.fighter_CGL.addWidget(self.fi_ch1_CGF)
        self.fi_ch1_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')
        fi_ch1_CGL = QtWidgets.QVBoxLayout(self.fi_ch1_CGF)

        self.fi_ch2_CGF = QtWidgets.QFrame(fighter_CGF)
        self.fi_ch2_CGF.setFixedWidth(155)
        self.fighter_CGL.addWidget(self.fi_ch2_CGF)
        self.fi_ch2_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')
        fi_ch2_CGL = QtWidgets.QVBoxLayout(self.fi_ch2_CGF)

        self.fi_ch3_CGF = QtWidgets.QFrame(fighter_CGF)
        self.fi_ch3_CGF.setFixedWidth(155)
        self.fighter_CGL.addWidget(self.fi_ch3_CGF)
        self.fi_ch3_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')
        fi_ch3_CGL = QtWidgets.QVBoxLayout(self.fi_ch3_CGF)

        self.fi_ch4_CGF = QtWidgets.QFrame(fighter_CGF)
        self.fi_ch4_CGF.setFixedWidth(155)
        self.fighter_CGL.addWidget(self.fi_ch4_CGF)
        self.fi_ch4_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')
        fi_ch4_CGL = QtWidgets.QVBoxLayout(self.fi_ch4_CGF)
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
            if "G:" in item.text() or "E:" in item.text():
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
            if "G:" in item.text() or "E:" in item.text():
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
            if "G:" in item.text() or "E:" in item.text():
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
            if "G:" in item.text() or "E:" in item.text():
                item.setStyleSheet("color: black; font: 18px; font-weight: bold");
            else:
                item.setStyleSheet("color: black; font: 14px;");
            fi_ch4_CGL.addWidget(item)

        #  copy params to check for changes
        # self.copied_params = deepcopy(global_parameter)
        self.copied_params = self.global_parameter[:]
        self.active_param = [-1, -1, -1, -1]


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
        timer.setInterval(50)
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
        self.stringArray_ch1[5].setText(str(self.global_label[1],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[0:8],'utf-8'))
        self.stringArray_ch1[6].setText(str(self.global_label[2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[8:16],'utf-8'))
        self.stringArray_ch1[7].setText(str(self.global_label[3],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[16:24],'utf-8'))
        self.stringArray_ch1[8].setText(str(self.global_label[4],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[24:32],'utf-8'))
        self.stringArray_ch1[9].setText("E: "+str(self.global_label[5],'utf-8'))
        self.stringArray_ch1[10].setText(str(self.global_label[6],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[32:40],'utf-8'))
        self.stringArray_ch1[11].setText(str(self.global_label[7],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[40:48],'utf-8'))
        self.stringArray_ch1[12].setText(str(self.global_label[8],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[48:56],'utf-8'))
        self.stringArray_ch1[13].setText(str(self.global_label[9],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[56:64],'utf-8'))
        self.stringArray_ch1[14].setText("E: "+str(self.global_label[10],'utf-8'))
        self.stringArray_ch1[15].setText(str(self.global_label[11],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[64:72],'utf-8'))
        self.stringArray_ch1[16].setText(str(self.global_label[12],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[72:80],'utf-8'))
        self.stringArray_ch1[17].setText(str(self.global_label[13],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[80:88],'utf-8'))
        self.stringArray_ch1[18].setText(str(self.global_label[14],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[88:96],'utf-8'))
        self.stringArray_ch1[19].setText("E: "+str(self.global_label[15],'utf-8'))
        self.stringArray_ch1[20].setText(str(self.global_label[16],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[96:104],'utf-8'))
        self.stringArray_ch1[21].setText(str(self.global_label[17],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[104:112],'utf-8'))
        self.stringArray_ch1[22].setText(str(self.global_label[18],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[112:120],'utf-8'))
        self.stringArray_ch1[23].setText(str(self.global_label[19],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[120:128],'utf-8'))


        self.stringArray_ch2[1].setText("Brightness : "+str(round(self.global_parameter[71],2)))
        self.stringArray_ch2[2].setText("Fade : "+str(round(self.global_parameter[72],2)))
        self.stringArray_ch2[3].setText("Shutter : "+str(round(self.global_parameter[73],2)))
        self.stringArray_ch2[4].setText("G: "+str(self.global_label[20],'utf-8'))
        self.stringArray_ch2[5].setText(str(self.global_label[21],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[128:136],'utf-8'))
        self.stringArray_ch2[6].setText(str(self.global_label[22],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[136:144],'utf-8'))
        self.stringArray_ch2[7].setText(str(self.global_label[23],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[144:152],'utf-8'))
        self.stringArray_ch2[8].setText(str(self.global_label[24],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[152:160],'utf-8'))
        self.stringArray_ch2[9].setText("E: "+str(self.global_label[25],'utf-8'))
        self.stringArray_ch2[10].setText(str(self.global_label[26],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[160:168],'utf-8'))
        self.stringArray_ch2[11].setText(str(self.global_label[27],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[168:176],'utf-8'))
        self.stringArray_ch2[12].setText(str(self.global_label[28],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[176:184],'utf-8'))
        self.stringArray_ch2[13].setText(str(self.global_label[29],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[184:192],'utf-8'))
        self.stringArray_ch2[14].setText("E: "+str(self.global_label[30],'utf-8'))
        self.stringArray_ch2[15].setText(str(self.global_label[31],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[192:200],'utf-8'))
        self.stringArray_ch2[16].setText(str(self.global_label[32],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[200:208],'utf-8'))
        self.stringArray_ch2[17].setText(str(self.global_label[33],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[208:216],'utf-8'))
        self.stringArray_ch2[18].setText(str(self.global_label[34],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[216:224],'utf-8'))
        self.stringArray_ch2[19].setText("E: "+str(self.global_label[35],'utf-8'))
        self.stringArray_ch2[20].setText(str(self.global_label[36],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[224:232],'utf-8'))
        self.stringArray_ch2[21].setText(str(self.global_label[37],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[232:240],'utf-8'))
        self.stringArray_ch2[22].setText(str(self.global_label[38],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[240:248],'utf-8'))
        self.stringArray_ch2[23].setText(str(self.global_label[39],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[248:256],'utf-8'))


        self.stringArray_ch3[1].setText("Brightness : "+str(round(self.global_parameter[101],2)))
        self.stringArray_ch3[2].setText("Fade : "+str(round(self.global_parameter[102],2)))
        self.stringArray_ch3[3].setText("Shutter : "+str(round(self.global_parameter[103],2)))
        self.stringArray_ch3[4].setText("G: "+str(self.global_label[40],'utf-8'))
        self.stringArray_ch3[5].setText(str(self.global_label[41],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[256:264],'utf-8'))
        self.stringArray_ch3[6].setText(str(self.global_label[42],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[264:272],'utf-8'))
        self.stringArray_ch3[7].setText(str(self.global_label[43],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[272:280],'utf-8'))
        self.stringArray_ch3[8].setText(str(self.global_label[44],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[280:288],'utf-8'))
        self.stringArray_ch3[9].setText("E: "+str(self.global_label[45],'utf-8'))
        self.stringArray_ch3[10].setText(str(self.global_label[46],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[288:296],'utf-8'))
        self.stringArray_ch3[11].setText(str(self.global_label[47],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[296:304],'utf-8'))
        self.stringArray_ch3[12].setText(str(self.global_label[48],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[304:312],'utf-8'))
        self.stringArray_ch3[13].setText(str(self.global_label[49],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[312:320],'utf-8'))
        self.stringArray_ch3[14].setText("E: "+str(self.global_label[50],'utf-8'))
        self.stringArray_ch3[15].setText(str(self.global_label[51],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[320:328],'utf-8'))
        self.stringArray_ch3[16].setText(str(self.global_label[52],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[328:336],'utf-8'))
        self.stringArray_ch3[17].setText(str(self.global_label[53],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[336:344],'utf-8'))
        self.stringArray_ch3[18].setText(str(self.global_label[54],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[344:352],'utf-8'))
        self.stringArray_ch3[19].setText("E: "+str(self.global_label[55],'utf-8'))
        self.stringArray_ch3[20].setText(str(self.global_label[56],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[352:360],'utf-8'))
        self.stringArray_ch3[21].setText(str(self.global_label[57],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[360:368],'utf-8'))
        self.stringArray_ch3[22].setText(str(self.global_label[58],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[368:376],'utf-8'))
        self.stringArray_ch3[23].setText(str(self.global_label[59],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[376:384],'utf-8'))


        self.stringArray_ch4[1].setText("Brightness : "+str(round(self.global_parameter[131],2)))
        self.stringArray_ch4[2].setText("Fade : "+str(round(self.global_parameter[132],2)))
        self.stringArray_ch4[3].setText("Shutter : "+str(round(self.global_parameter[133],2)))
        self.stringArray_ch4[4].setText("G: "+str(self.global_label[60],'utf-8'))
        self.stringArray_ch4[5].setText(str(self.global_label[61],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[384:392],'utf-8'))
        self.stringArray_ch4[6].setText(str(self.global_label[62],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[392:400],'utf-8'))
        self.stringArray_ch4[7].setText(str(self.global_label[63],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[400:408],'utf-8'))
        self.stringArray_ch4[8].setText(str(self.global_label[64],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[408:416],'utf-8'))
        self.stringArray_ch4[9].setText("E: "+str(self.global_label[65],'utf-8'))
        self.stringArray_ch4[10].setText(str(self.global_label[66],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[416:424],'utf-8'))
        self.stringArray_ch4[11].setText(str(self.global_label[67],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[424:432],'utf-8'))
        self.stringArray_ch4[12].setText(str(self.global_label[68],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[432:440],'utf-8'))
        self.stringArray_ch4[13].setText(str(self.global_label[69],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[440:448],'utf-8'))
        self.stringArray_ch4[14].setText("E: "+str(self.global_label[70],'utf-8'))
        self.stringArray_ch4[15].setText(str(self.global_label[71],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[448:456],'utf-8'))
        self.stringArray_ch4[16].setText(str(self.global_label[72],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[456:464],'utf-8'))
        self.stringArray_ch4[17].setText(str(self.global_label[73],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[464:472],'utf-8'))
        self.stringArray_ch4[18].setText(str(self.global_label[74],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[472:480],'utf-8'))
        self.stringArray_ch4[19].setText("E: "+str(self.global_label[75],'utf-8'))
        self.stringArray_ch4[20].setText(str(self.global_label[76],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[480:488],'utf-8'))
        self.stringArray_ch4[21].setText(str(self.global_label[77],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[488:496],'utf-8'))
        self.stringArray_ch4[22].setText(str(self.global_label[78],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[496:504],'utf-8'))
        self.stringArray_ch4[23].setText(str(self.global_label[79],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[504:512],'utf-8'))

        # check for last changed value
        #index_changed = np.where((np.array(self.copied_params) == np.array(self.global_parameter)) == False)[0]

        active_menu = [*self.global_parameter[201:205]]
        #print('active:', active_menu)

        # colors for each area
        oncolor = ['#ffa500', '#ffff00', '#00cc00', '#00dcff']
        offcolor = ['#ffe4b2', '#ffffb2', '#b2efb2', '#b2f4ff']

        for active, channel in zip(active_menu, [self.stringArray_ch1, self.stringArray_ch2, self.stringArray_ch3, self.stringArray_ch4]):
            # reset
            for i ,j, k, l in zip(channel[4:9], channel[9:14], channel[14:19], channel[19:24]):
                i.setStyleSheet("color: black; font: 18px; background-color: "+offcolor[0])
                j.setStyleSheet("color: black; font: 18px; background-color: "+offcolor[1])
                k.setStyleSheet("color: black; font: 18px; background-color: "+offcolor[2])
                l.setStyleSheet("color: black; font: 18px; background-color: "+offcolor[3])

            if active == 0:
                for i in channel[4:9]:
                    i.setStyleSheet("font-weight: bold; color: black; font: 20px; background-color: "+oncolor[0])
            elif active == 1:
                for i in channel[9:14]:
                    i.setStyleSheet("font-weight: bold; color: black; font: 20px; background-color: "+oncolor[1])
            elif active == 2:
                for i in channel[14:19]:
                    i.setStyleSheet("font-weight: bold; color: black; font: 20px; background-color: "+oncolor[2])
            elif active == 3:
                for i in channel[19:24]:
                    i.setStyleSheet("font-weight: bold; color: black; font: 20px; background-color: "+oncolor[3])

        if self.global_parameter[40] == 0:
            self.fi_ch1_CGF.setStyleSheet('background-color: rgba(75, 75, 75, 1);')
        elif self.global_parameter[40] == 1:
            self.fi_ch1_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')

        if self.global_parameter[70] == 0:
            self.fi_ch2_CGF.setStyleSheet('background-color: rgba(75, 75, 75, 1);')
        elif self.global_parameter[70] == 1:
            self.fi_ch2_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')

        if self.global_parameter[100] == 0:
            self.fi_ch3_CGF.setStyleSheet('background-color: rgba(75, 75, 75, 1);')
        elif self.global_parameter[100] == 1:
            self.fi_ch3_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')

        if self.global_parameter[130] == 0:
            self.fi_ch4_CGF.setStyleSheet('background-color: rgba(75, 75, 75, 1);')
        elif self.global_parameter[130] == 1:
            self.fi_ch4_CGF.setStyleSheet('background-color: rgba(175, 175, 175, 1);')

        self.copied_params = self.global_parameter[:]
