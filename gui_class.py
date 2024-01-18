import time
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
from labels import labels as t_labels
from labels_2d import labels as t_labels_2d
from multiprocessing import shared_memory

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, array, label , mode, parent = None):

        # some settings
        channels = [1,2,3,4]

        # in 2d mode, we need other labels
        if mode == '2d':
            self.labels = t_labels_2d
        else:
            self.labels = t_labels

        # initialize window
        super(MainWindow, self).__init__()

        # get global array for parameters of all generators
        # and effects
        self.global_parameter    = array
        self.globalold_parameter = np.zeros(255)

        # get labels for all buttons
        self.global_label = label

        # get array of currently shown gui values
        # what is this?
        self.shared_mem_gui_vals     = shared_memory.SharedMemory(name = "GuiValues1")
        self.shared_mem_gui_vals_old = shared_memory.SharedMemory(name = "GuiValues1")

        # initialize layout
        # creating main container-frame, parent it to QWindow
        self.main_CF = QtWidgets.QFrame(self)
        self.main_CF.setStyleSheet('background-color: rgba(50, 50, 50, 1)')
        self.setCentralWidget(self.main_CF)

        # creating layout and parent it to main container
        # is it correct, that main_CL now manages children of main_CF ?
        self.main_CL = QtWidgets.QHBoxLayout(self.main_CF)
        # creating vertical Layer for launchpad and utility panel
        self.vert_CF = QtWidgets.QFrame(self)
        self.vert_CL = QtWidgets.QVBoxLayout(self.vert_CF)

        # update gui values in regular intervals
        # this is what?
        self.update = 0

        # ----------------------------------------
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
                       [  '0','255','255', '0.8'],
                       ['255',  '0',  '0', '0.8'], # global presets
                       ['255','255',  '0', '0.8'], # global effect 1
                       [  '0','255',  '0', '0.8'], # global effect 2
                       [  '0','255','255', '0.8'], # global effect 3
                       ['255',  '0',  '0', '0.8']]

        launchpad_CGF = QtWidgets.QFrame(self.main_CF)
        self.vert_CL.addWidget(launchpad_CGF)
        self.padlabels[x][y].setStyleSheet('background-color: rgba('+', '.join(self.colors[0])+');')

        launchpad_CGL = QtWidgets.QGridLayout(launchpad_CGF)
        launchpad_CGL.setContentsMargins(0,0,0,0)
        for x in range(8):
            for y in range(8):
                launchpad_CGL.addWidget(self.padlabels[x][y],x,y)

        # ----------------------------------------
        # utility area under launchpad
        utility_CGF = QtWidgets.QFrame(self.main_CF)

        self.vert_CL.addWidget(utility_CGF)

        self.utilitylabels = []
        for x in range(10):
            temp = []
            for y in range(4):
                label = QtWidgets.QLabel('')
                label.setWordWrap(True)
                label.setStyleSheet("background-color: rgba(0,0,0,0.0);")
                temp.append(label)

            self.utilitylabels.append(temp)

        # ----------------------------------------
        # what is this?
        utility_CGL = QtWidgets.QGridLayout(utility_CGF)

        for x in range(10):
            for y in range(4):
                utility_CGL.addWidget(self.utilitylabels[x][y],x,y)

        # adding vert_CL
        self.main_CL.addWidget(self.vert_CF)

        # ----------------------------------------
        # doing the same with a third container(MIDIFIGHTER)

        fighter_CGF = QtWidgets.QFrame(self.main_CF)
        self.main_CL.addWidget(fighter_CGF)
        fighter_CGF.setStyleSheet('background-color: rgba(150, 150, 150, 1);')
        self.fighter_CGL = QtWidgets.QHBoxLayout(fighter_CGF)

        # create sub-containers for fighter channels 1-4
        self.fighter_channels = {}
        for channel in channels:
            self.fighter_channels[channel] = QtWidgets.QFrame(fighter_CGF)

        fighter_channel_list = {}
        for channel in self.fighter_channels.keys():
            self.fighter_channels[channel].setFixedWidth(155)
            self.fighter_CGL.addWidget(self.fighter_channels[channel])
            self.fighter_channels[channel].setStyleSheet('background-color: rgba(175, 175, 175, 1);')
            fighter_channel_list[channel] = QtWidgets.QVBoxLayout(self.fighter_channels[channel])

        # ----------------------------------------
        # create all labels for the right panel

        self.stringArray = {}

        for channel in channels:
            self.stringArray[channel] = []
            self.stringArray[channel].append(QtWidgets.QLabel("Channel "+str(channel)))
            self.stringArray[channel].append(QtWidgets.QLabel("Brightness : 127"))
            self.stringArray[channel].append(QtWidgets.QLabel("Fade : 0"))
            self.stringArray[channel].append(QtWidgets.QLabel("Shutter : 0"))
            self.stringArray[channel].append(QtWidgets.QLabel("Generator : DUMMY"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 1 : 89"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 2 : 54"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 3 : 110"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 4 : 110"))
            self.stringArray[channel].append(QtWidgets.QLabel("Effect 1 : DUMMY"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 1 : 0"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 2 : 127"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 3 : 110"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 4 : 110"))
            self.stringArray[channel].append(QtWidgets.QLabel("Effect 2 : DUMMY"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 1 : 0"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 2 : 127"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 3 : 110"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 4 : 110"))
            self.stringArray[channel].append(QtWidgets.QLabel("Effect 3 : DUMMY"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 1 : 0"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 2 : 127"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 3 : 110"))
            self.stringArray[channel].append(QtWidgets.QLabel("Parameter 4 : 110"))

#        for channel, fi in zip(self.stringArray.keys(),
#                            [fi_ch1_CGL, fi_ch2_CGL, fi_ch3_CGL, fi_ch4_CGL]):
            for item in self.stringArray[channel]:
                if "G:" in item.text() or "E:" in item.text():
                    item.setStyleSheet("color: black; font: 16px; font-weight: bold; font-family: Manjari;");
                else:
                    item.setStyleSheet("color: black; font: 14px;; font-family: Manjari;");
                fighter_channel_list[channel].addWidget(item)

        # copy params to check for changes
        # self.copied_params = deepcopy(global_parameter)
        self.copied_params = self.global_parameter[:]
        self.active_param  = [-1, -1, -1, -1]

        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.main_CL)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.conditional_update)
        timer.setInterval(40)
        timer.start()


    def conditional_update(self):
        '''filter GUI update for value change'''
        #print(self.global_parameter[20], self.globalold_parameter[20])
        self.update += 1
        if any(self.globalold_parameter != self.global_parameter) or self.shared_mem_gui_vals != self.shared_mem_gui_vals_old  or self.update > 50:
            self.shared_mem_gui_vals_old = self.shared_mem_gui_vals
            #print("something changed")
            self.update_fighter_values()
            self.update_global_values()
            self.update_launchpad_values()

            for i in range(255):
                self.globalold_parameter[i] = self.global_parameter[i]

            self.update = 0


    def start_Renderer(self):
        """Routine to start all threads
        """
        self.global_parameter[0] = 0
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

    def update_global_values(self):
        self.utilitylabels[0][0].setText("Global Bright: "+str(round(self.global_parameter[1],2)))
        self.utilitylabels[1][0].setText("Sound Gain: "+str(round(self.global_parameter[19],2)))
        self.utilitylabels[2][0].setText("Normalize")
        self.utilitylabels[3][0].setText("AutoPilot (s): "+str(int(round(2+self.global_parameter[6]*180,0))))
        self.utilitylabels[4][0].setText("AutoPilot On/Off: "+str(round(self.global_parameter[5],2)))
        if(self.global_parameter[5]>0):
            self.utilitylabels[4][0].setStyleSheet("background-color: #00cc00;")
        else:
            self.utilitylabels[4][0].setStyleSheet("background-color: #ffa500;")
        self.utilitylabels[5][0].setText("E1: "+str(self.global_label[80],'utf-8'))
        self.utilitylabels[5][0].setStyleSheet("background-color: #ffff00;")
        self.utilitylabels[0][1].setText("E2: "+str(self.global_label[85],'utf-8'))
        self.utilitylabels[0][1].setStyleSheet("background-color: #00cc00;")
        self.utilitylabels[5][1].setText("E3: "+str(self.global_label[90],'utf-8'))
        self.utilitylabels[5][1].setStyleSheet("background-color: #00dcff;")

        #ffffb2', '#b2efb2', '#b2f4ff #ffff00', '#00cc00', '#00dcff
        for i in range(4):
            self.utilitylabels[6+i][0].setText(str(self.global_label[81+i],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[512+i*8:520+i*8],'utf-8'))
            self.utilitylabels[6+i][0].setStyleSheet("background-color: #ffffb2;")
            self.utilitylabels[1+i][1].setText(str(self.global_label[86+i],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[544+i*8:552+i*8],'utf-8'))
            self.utilitylabels[1+i][1].setStyleSheet("background-color: #b2efb2;")
            self.utilitylabels[6+i][1].setText(str(self.global_label[91+i],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[576+i*8:584+i*8],'utf-8'))
            self.utilitylabels[6+i][1].setStyleSheet("background-color: #b2f4ff;")


    def update_launchpad_values(self):

        # get labels of active menu
        # this is given by self.global_parameter[200]
        current_labels = self.labels[int(self.global_parameter[200]), :, :]

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

                # menu is closed
                if self.global_parameter[200] == 0:
                    self.padlabels[x][y].setStyleSheet('background-color: rgb(100, 100, 100); text-align: center;')
                    # colored background for oneshots
                    if y > 4 and x == 2:
                        self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 0, 0); text-align: center;')
                    elif y > 4 and x == 3:
                        self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 0, 0); text-align: center;')
                    elif y > 4 and x == 4:
                        self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 0, 0); text-align: center;')
                    elif y > 6 and x == 5:
                        self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 0, 0); text-align: center;')
                    #presets
                    elif x == 0 and y < 4:
                        self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 0, 0); text-align: center;')
                        self.padlabels[x][y].setText('Channel '+str(y+1)+'\nPresets')
                    elif x == 0 and y == 4:
                        self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 0, 0); text-align: center;')
                        self.padlabels[x][y].setText('Global\nPresets')
                    elif x == 0 and y == 5:
                        self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 0, 0); text-align: center;')
                        self.padlabels[x][y].setText('Global\nPresets 2')
                    #start
                    elif x == 0 and y == 7:
                        self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 0, 255); text-align: center;')
                        self.padlabels[x][y].setText('Start')
                    #generators
                    elif x == 1 and y < 4:
                        self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 128, 0); text-align: center;')
                        self.padlabels[x][y].setText('Generator')
                    # effects 1
                    elif x == 2 and y < 5:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 255, 0); text-align: center;')
                            self.padlabels[x][y].setText('FX 1')
                    # effects 2
                    elif x == 3 and y < 5:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(0, 255, 0); text-align: center;')
                            self.padlabels[x][y].setText('FX 2')
                    # effects 3
                    elif x == 4 and y < 5:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(0, 255, 255); text-align: center;')
                            self.padlabels[x][y].setText('FX 3')
                    # paste
                    elif x == 5 and y < 4:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(0, 0, 255); text-align: center;')
                            self.padlabels[x][y].setText('Paste')
                    # copy
                    elif x == 6 and y < 4:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 0, 255); text-align: center;')
                            self.padlabels[x][y].setText('Copy')
                    # save presets
                    elif x == 7 and y < 5:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 255, 255); text-align: center;')
                            self.padlabels[x][y].setText('Save')
                    # autopilot
                    elif x == 7 and y == 7:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 255, 255); text-align: center;')
                            self.padlabels[x][y].setText('AutoPilot')
                    # random
                    elif x == 7 and y == 5:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(0, 255, 0); text-align: center;')
                            self.padlabels[x][y].setText('Mutate CH1')
                    # global effects 1
                    elif x == 7 and y == 6:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(255, 255, 0); text-align: center;')
                            self.padlabels[x][y].setText('Global FX')
                    # quicksave & load
                    elif x == 6 and y == 7:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(0, 255, 0); text-align: center;')
                            self.padlabels[x][y].setText('Quickload')
                    elif x == 6 and y == 6:
                            self.padlabels[x][y].setStyleSheet('background-color: rgb(0, 255, 0); text-align: center;')
                            self.padlabels[x][y].setText('Quicksave')

                else:
                    # get color - don't do a shallow copy here!
                    color = self.colors[int(self.global_parameter[200])][:]

                    if x in [2, 5] or y in [2, 5]:
                        for i in range(3):
                            color[i] = str(np.clip(int(color[i]) - 50, 0, 255))

                    if counter == ind + 1:
                        # active generator/effect gets red border
                        self.padlabels[x][y].setStyleSheet('Background-color: rgba('+', '.join(color)+'); color: red; border-style: dashed; border-width: 4px; border-color: white; text-align: center;')
                    else:
                        self.padlabels[x][y].setStyleSheet('background-color: rgba('+', '.join(color)+'); text-align: center;')

                counter+=1


    def update_fighter_values(self):

        # loop over dictionary with fighter channels
        for channel in self.stringArray.keys():
            # calculate several offsets to point
            # to the right position in arrays
            off_1 = (channel-1)*30
            off_2 = (channel-1)*20
            off_3 = (channel-1)*128

            self.stringArray[channel][1].setText("Brightness : "+str(round(self.global_parameter[41 + off_1],2)))
            self.stringArray[channel][2].setText("Fade : "      +str(round(self.global_parameter[42 + off_1],2)))
            self.stringArray[channel][3].setText("Shutter : "   +str(round(self.global_parameter[43 + off_1],2)))
            self.stringArray[channel][4].setText("G: "+str(self.global_label[0 + off_2],'utf-8'))
            self.stringArray[channel][5].setText(str(self.global_label[1 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+0:off_3+8],'utf-8'))
            self.stringArray[channel][6].setText(str(self.global_label[2 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+8:off_3+16],'utf-8'))
            self.stringArray[channel][7].setText(str(self.global_label[3 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+16:off_3+24],'utf-8'))
            self.stringArray[channel][8].setText(str(self.global_label[4 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+24:off_3+32],'utf-8'))
            self.stringArray[channel][9].setText("E: "+str(self.global_label[5 + off_2],'utf-8'))
            self.stringArray[channel][10].setText(str(self.global_label[6 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+32:off_3+40],'utf-8'))
            self.stringArray[channel][11].setText(str(self.global_label[7 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+40:off_3+48],'utf-8'))
            self.stringArray[channel][12].setText(str(self.global_label[8 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+48:off_3+56],'utf-8'))
            self.stringArray[channel][13].setText(str(self.global_label[9 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+56:off_3+64],'utf-8'))
            self.stringArray[channel][14].setText("E: "+str(self.global_label[10 + off_2],'utf-8'))
            self.stringArray[channel][15].setText(str(self.global_label[11 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+64:off_3+72],'utf-8'))
            self.stringArray[channel][16].setText(str(self.global_label[12 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+72:off_3+80],'utf-8'))
            self.stringArray[channel][17].setText(str(self.global_label[13 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+80:off_3+88],'utf-8'))
            self.stringArray[channel][18].setText(str(self.global_label[14 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+88:off_3+96],'utf-8'))
            self.stringArray[channel][19].setText("E: "+str(self.global_label[15 + off_2],'utf-8'))
            self.stringArray[channel][20].setText(str(self.global_label[16 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+96:off_3+104],'utf-8'))
            self.stringArray[channel][21].setText(str(self.global_label[17 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+104:off_3+112],'utf-8'))
            self.stringArray[channel][22].setText(str(self.global_label[18 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+112:off_3+120],'utf-8'))
            self.stringArray[channel][23].setText(str(self.global_label[19 + off_2],'utf-8')+" : "+str(self.shared_mem_gui_vals.buf[off_3+120:off_3+128],'utf-8'))

        # check for last changed value
        #index_changed = np.where((np.array(self.copied_params) == np.array(self.global_parameter)) == False)[0]

        active_menu = [*self.global_parameter[201:205]]
        #print('active:', active_menu)

        # colors for each area
        oncolor = ['#ffa500', '#ffff00', '#00cc00', '#00dcff']
        offcolor = ['#ffe4b2', '#ffffb2', '#b2efb2', '#b2f4ff']

        for active, channel in zip(active_menu, [self.stringArray[1], self.stringArray[2], self.stringArray[3], self.stringArray[4]]):
            # reset
            for i ,j, k, l in zip(channel[4:9], channel[9:14], channel[14:19], channel[19:24]):
                i.setStyleSheet("color: black; font: 16px; font-family: Manjari; background-color: "+offcolor[0])
                j.setStyleSheet("color: black; font: 16px; font-family: Manjari; background-color: "+offcolor[1])
                k.setStyleSheet("color: black; font: 16px; font-family: Manjari; background-color: "+offcolor[2])
                l.setStyleSheet("color: black; font: 16px; font-family: Manjari; background-color: "+offcolor[3])

            if active == 0:
                for i in channel[4:9]:
                    i.setStyleSheet("font-weight: bold; color: black; font: 16px; font-family: Manjari; background-color: "+oncolor[0])
            elif active == 1:
                for i in channel[9:14]:
                    i.setStyleSheet("font-weight: bold; color: black; font: 16px; font-family: Manjari; background-color: "+oncolor[1])
            elif active == 2:
                for i in channel[14:19]:
                    i.setStyleSheet("font-weight: bold; color: black; font: 16px; font-family: Manjari; background-color: "+oncolor[2])
            elif active == 3:
                for i in channel[19:24]:
                    i.setStyleSheet("font-weight: bold; color: black; font: 16px; font-family: Manjari; background-color: "+oncolor[3])

        # switch active color
        for channel, i in zip(self.fighter_channels.keys(), [40,70,100,130]):
            if self.global_parameter[i] == 0:
                self.fighter_channels[channel].setStyleSheet('background-color: rgba(75, 75, 75, 1);')
            elif self.global_parameter[i] == 1:
                self.fighter_channels[channel].setStyleSheet('background-color: rgba(175, 175, 175, 1);')

        self.copied_params = self.global_parameter[:]
