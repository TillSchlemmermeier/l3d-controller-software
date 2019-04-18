#! /usr/bin/python3.5

from tkinter.ttk import Combobox
from tkinter import *

from cube_utils import *
# from cube_animations import rain_gen, gen_dots, plain_gen
# from cube_interactive import dots_on_sphere, random, sphere, speed_decorator, hsphere, planes, lines, cube, corner, circle, blur, moveandfade, seperate, blow, random_lines
from cube_rgb import createRGBWorld, combineRGBWorlds, manipulateRGBWorld, generateRainbowWorld
# from cube_effects import *
# from cube_generators import *
from math import *
import serial
import sys, os, glob  # , time
import numpy as np
import struct
import inspect
from rtmidi.midiutil import open_midiinput,open_midioutput
# from copy import deepcopy
from CubeWorld import CubeWorld
# from time import sleep
import time as time
import pyaudio

MidiKey = 0
MidiValue = 0


# sound2light stuff ende

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        frame = Frame(self)
        frame.pack()

        #Arduino CONECTION
        try:
            self.con =  serial.Serial('/dev/ttyACM0', 230400)
            print(self.con)
        except IOError:
            self.con = serial.Serial('/dev/ttyACM1', 230400)
            print(self.con)

        #DMX CONECTION
        #try:
        #    self.dmx =  serial.Serial('/dev/ttyUSB0', 57600)
        #    print(self.dmx)
        #except IOError:
        #    self.dmx = serial.Serial('/dev/ttyUSB11', 57600)
        #    print(self.dmx)

        # VARS
        self.do_send = False
        self.do_send_rgb = False
        self.sendSpeed = 20

        self.cubeWorld = CubeWorld()
        self.world = np.zeros([3, 10, 10, 10])
        self.send_header = []
        self.framecount = 1
        self.send_array_rgb = []
        # self.send_list =[]
        self.artnet_switch = IntVar()   # callback variable for artnet switch
        self.artnet_color_switch = IntVar()   # callback variable for artnet switch

	# load generators and effects
        self.generators = ["g_blank", "g_cube", "g_random", "g_growing_sphere","g_orbiter","g_randomlines",
                           "g_sphere", "g_snake","g_planes", "g_planes_falling", "g_corner", "g_corner_grow",
                           "g_shooting_star", "g_orbiter2", "g_randomcross",  "g_growing_corner",
                           "g_rain", "g_circles", "g_falling", "g_obliqueplane", "g_obliqueplaneXYZ", "g_smiley",
                           "g_torusrotation","g_growingface","g_pyramid", "g_orbiter3","g_gauss","g_wave",
                           "g_drop", "g_pyramid_upsidedown", 'g_cube_edges', 'a_orbbot', 'a_squares_cut',
                           'a_lines', 'a_pulsating', 'a_multi_cube_edges', 'g_squares', 'g_rotate_plane',
                           'a_random_cubes', 'g_soundcube', 'g_cut', 'g_bouncy', 'g_darksphere', 'g_sound_sphere',
                           'g_trees', 'g_rising_square', 'g_inandout', 'g_soundrandom', 'g_orbiter_big', 'g_centralglow',
                           'g_sound_grow', 'g_edgeglow', 'g_spiral']

        self.effects = ["e_blank","e_fade2blue","e_rainbow","e_staticcolor", "e_violetblue", "e_redyellow",
                        "e_tremolo", "e_gradient", "e_prod_saturation", "e_prod_hue",
                        "e_bright_osci", 'e_cut_cube', 'e_rare_strobo', 'e_s2l', 'e_remove_random']

	# sort generators and effects
        self.generators.sort()
        self.effects.sort()

        # Header Information
        self.hSpeed = 1
        self.hBright = 200
        self.hPal = 116
        self.hPalMode = 0
        self.hRGBMode = 1

        self.send_array_rgb = bytearray(3009)

        self.MidiButtonListBool = {1:False,4:False,7:False,10:False,13:False,16:False,19:False,22:False,3:False,6:False,9:False,12:False,15:False,18:False,21:False,24:False}

        #self.funkyImage = Text(frame)
        #img = BitmapImage( file='l3dBanner.bmp')
        ###self.funkyImage.image_create(END, image = img)
        #self.funkyImage.grid(row=10, column=3)

        self.font='Arial'
        '''
        self.pic0 = PhotoImage(file='banner/l3dbanner-0.png')
        self.imgLabel0 = Label(frame,image=self.pic0)
        self.imgLabel0.grid(row=10,column=0)

        self.pic1 = PhotoImage(file='banner/l3dbanner-1.png')
        self.imgLabel1 = Label(frame,image=self.pic1)
        self.imgLabel1.grid(row=10,column=1)

        self.pic2 = PhotoImage(file='banner/l3dbanner-2.png')
        self.imgLabel2 = Label(frame,image=self.pic2)
        self.imgLabel2.grid(row=10,column=2)

        self.pic3 = PhotoImage(file='banner/l3dbanner-3.png')
        self.imgLabel3 = Label(frame,image=self.pic3)
        self.imgLabel3.grid(row=10,column=3)

        self.pic4 = PhotoImage(file='banner/l3dbanner-4.png')
        self.imgLabel4 = Label(frame,image=self.pic4)
        self.imgLabel4.grid(row=10,column=4)

        self.pic5 = PhotoImage(file='banner/l3dbanner-5.png')
        self.imgLabel5 = Label(frame,image=self.pic5)
        self.imgLabel5.grid(row=10,column=5)
        '''
        #
        ## GUI Callabcks
        def optionmenuG1_selection(event):
            self.cubeWorld.set_Genenerator("A", self.dropdownG1.get(),0)
            pass

        def optionmenuG2_selection(event):
            self.cubeWorld.set_Genenerator("B", self.dropdownG2.get(),0)
            pass

        def optionmenuG3_selection(event):
            self.cubeWorld.set_Genenerator("C", self.dropdownG3.get(),0)
            pass

        def optionmenuE11_selection(event):
            self.cubeWorld.set_Genenerator("A", self.dropdownE11Current.get(),1)
            pass

        def optionmenuE12_selection(event):
            self.cubeWorld.set_Genenerator("B", self.dropdownE12Current.get(),1)
            pass

        def optionmenuE13_selection(event):
            self.cubeWorld.set_Genenerator("C", self.dropdownE13Current.get(),1)
            pass

        def optionmenuE21_selection(event):
            self.cubeWorld.set_Genenerator("A", self.dropdownE21Current.get(),2)
            pass

        def optionmenuE22_selection(event):
            self.cubeWorld.set_Genenerator("B", self.dropdownE22Current.get(),2)
            pass

        def optionmenuE23_selection(event):
            self.cubeWorld.set_Genenerator("C", self.dropdownE23Current.get(),2)
            pass

        # GUI Elements
        self.startButton = Button(frame, text="Start", command=self.startsending)
        self.startButton.grid(row=0, column=4)

        self.stopButton = Button(frame, text="Stop", command=self.stopsending)
        self.stopButton.grid(row=0, column=5)

        self.BrightnesValue = StringVar()
        self.ShutterValue = StringVar()
        self.Brightnes = Label(frame, textvariable=self.BrightnesValue)
        self.Brightnes.grid(row=0, column=0)
        self.Shutter = Label(frame, textvariable=self.ShutterValue)
        self.Shutter.grid(row=0, column=1)

        self.artnetCheckbox = Checkbutton(frame, text="Artnet Control",
                                          variable=self.artnet_switch,
                                          command=self.checkbox_callback,
                                          onvalue=True,
                                          offvalue=False)
        self.artnetCheckbox.grid(row=0,column=2)

        self.artnetcolorCheckbox = Checkbutton(frame, text="Artnet Color Control",
                                          variable=self.artnet_color_switch,
                                          command=self.checkbox_color_callback,
                                          onvalue=True,
                                          offvalue=False)

        self.artnetcolorCheckbox.grid(row=0,column=3)

        self.labelG1 = Label(frame, text="Generator A",font=(self.font, "12"))
        self.labelG1.grid(row=1, column=0)

        self.labelG2 = Label(frame, text="Generator B",font=(self.font, "12"))
        self.labelG2.grid(row=1, column=3)

        self.labelG3 = Label(frame, text="Generator C",font=(self.font, "12"))
        self.labelG3.grid(row=1, column=6)

        self.labelE11 = Label(frame, text="Effekt A 1",font=(self.font, "12"))
        self.labelE11.grid(row=1, column=1)

        self.labelE12 = Label(frame, text="Effekt B 1",font=(self.font, "12"))
        self.labelE12.grid(row=1, column=4)

        self.labelE13 = Label(frame, text="Effekt C 1",font=(self.font, "12"))
        self.labelE13.grid(row=1, column=7)

        self.labelE21 = Label(frame, text="Effekt A 2",font=(self.font, "12"))
        self.labelE21.grid(row=1, column=2)

        self.labelE22 = Label(frame, text="Effekt B 2",font=(self.font, "12"))
        self.labelE22.grid(row=1, column=5)

        self.labelE23 = Label(frame, text="Effekt C 2",font=(self.font, "12"))
        self.labelE23.grid(row=1, column=8)

        self.dropdownG1Current = StringVar()
        self.G1param1String = StringVar()
        self.G1param2String = StringVar()
        self.G1param3String = StringVar()
        self.dropdownG1Current.set(self.generators[0])
#        self.dropdownG1 = OptionMenu(frame, self.dropdownG1Current, *self.generators, command = optionmenuG1_selection)
        self.dropdownG1 = Combobox(frame, values = self.generators)
        self.dropdownG1.bind("<<ComboboxSelected>>", optionmenuG1_selection)
        #, command = optionmenuG1_selection)
        self.dropdownG1.grid(row=2, column=0,sticky="ew")
        self.G1param1 = Label(frame, textvariable=self.G1param1String ,font=(self.font, "12"))
        self.G1param1.grid(row=3, column=0)
        self.G1param2 = Label(frame, textvariable=self.G1param2String ,font=(self.font, "12"))
        self.G1param2.grid(row=4, column=0)
        self.G1param3 = Label(frame, textvariable=self.G1param3String ,font=(self.font, "12"))
        self.G1param3.grid(row=5, column=0)

        self.dropdownG2Current = StringVar()
        self.G2param1String = StringVar()
        self.G2param2String = StringVar()
        self.G2param3String = StringVar()
        self.dropdownG2Current.set(self.generators[0])
        #self.dropdownG2 = OptionMenu(frame, self.dropdownG2Current, *self.generators,command = optionmenuG2_selection)
        self.dropdownG2 = Combobox(frame, values = self.generators)
        self.dropdownG2.bind("<<ComboboxSelected>>", optionmenuG2_selection)
        self.dropdownG2.grid(row=2, column=3,sticky="ew")
        self.G2param1 = Label(frame, textvariable=self.G2param1String ,font=(self.font, "12"))
        self.G2param1.grid(row=3, column=3)
        self.G2param2 = Label(frame, textvariable=self.G2param2String ,font=(self.font, "12"))
        self.G2param2.grid(row=4, column=3)
        self.G2param3 = Label(frame, textvariable=self.G2param3String,font=(self.font, "12"))
        self.G2param3.grid(row=5, column=3)

        self.dropdownG3Current = StringVar()
        self.G3param1String = StringVar()
        self.G3param2String = StringVar()
        self.G3param3String = StringVar()
        self.dropdownG3Current.set(self.generators[0])
        #self.dropdownG3 = OptionMenu(frame, self.dropdownG3Current, *self.generators,command = optionmenuG3_selection)
        self.dropdownG3 = Combobox(frame, values = self.generators)
        self.dropdownG3.bind("<<ComboboxSelected>>", optionmenuG3_selection)
        self.dropdownG3.grid(row=2, column=6,sticky="ew")
        self.G3param1 = Label(frame, textvariable=self.G3param1String,font=(self.font, "12"))
        self.G3param1.grid(row=3, column=6)
        self.G3param2 = Label(frame, textvariable=self.G3param2String,font=(self.font, "12"))
        self.G3param2.grid(row=4, column=6)
        self.G3param3 = Label(frame, textvariable=self.G3param3String,font=(self.font, "12"))
        self.G3param3.grid(row=5, column=6)

        self.dropdownE11Current = StringVar()
        self.E11param1String = StringVar()
        self.E11param2String = StringVar()
        self.E11param3String = StringVar()
        self.dropdownE11Current.set(self.effects[0])
        self.dropdownE11 = OptionMenu(frame, self.dropdownE11Current, *self.effects,command = optionmenuE11_selection)
        self.dropdownE11.grid(row=2, column=1,sticky="ew")
        self.E11param1 = Label(frame, textvariable=self.E11param1String,font=(self.font, "12"))
        self.E11param1.grid(row=3, column=1)
        self.E11param2 = Label(frame, textvariable=self.E11param2String,font=(self.font, "12"))
        self.E11param2.grid(row=4, column=1)
        self.E11param3 = Label(frame, textvariable=self.E11param3String,font=(self.font, "12"))
        self.E11param3.grid(row=5, column=1)

        self.dropdownE12Current = StringVar()
        self.E12param1String = StringVar()
        self.E12param2String = StringVar()
        self.E12param3String = StringVar()
        self.dropdownE12Current.set(self.effects[0])
        self.dropdownE12 = OptionMenu(frame, self.dropdownE12Current, *self.effects, command = optionmenuE12_selection)
        self.dropdownE12.grid(row=2, column=4,sticky="ew")
        self.E12param1 = Label(frame, textvariable=self.E12param1String,font=(self.font, "12"))
        self.E12param1.grid(row=3, column=4)
        self.E12param2 = Label(frame, textvariable=self.E12param2String,font=(self.font, "12"))
        self.E12param2.grid(row=4, column=4)
        self.E12param3 = Label(frame, textvariable=self.E12param3String,font=(self.font, "12"))
        self.E12param3.grid(row=5, column=4)

        self.dropdownE13Current = StringVar()
        self.E13param1String = StringVar()
        self.E13param2String = StringVar()
        self.E13param3String = StringVar()
        self.dropdownE13Current.set(self.effects[0])
        self.dropdownE13 = OptionMenu(frame, self.dropdownE13Current, *self.effects, command = optionmenuE13_selection)
        self.dropdownE13.grid(row=2, column=7,sticky="ew")
        self.E13param1 = Label(frame, textvariable=self.E13param1String,font=(self.font, "12"))
        self.E13param1.grid(row=3, column=7)
        self.E13param2 = Label(frame, textvariable=self.E13param2String,font=(self.font, "12"))
        self.E13param2.grid(row=4, column=7)
        self.E13param3 = Label(frame, textvariable=self.E13param3String,font=(self.font, "12"))
        self.E13param3.grid(row=5, column=7)

        self.dropdownE21Current = StringVar()
        self.E21param1String = StringVar()
        self.E21param2String = StringVar()
        self.E21param3String = StringVar()
        self.dropdownE21Current.set(self.effects[0])
        self.dropdownE21 = OptionMenu(frame, self.dropdownE21Current, *self.effects,command = optionmenuE21_selection)
        self.dropdownE21.grid(row=2, column=2,sticky="ew")
        self.E21param1 = Label(frame, textvariable=self.E21param1String,font=(self.font, "12"))
        self.E21param1.grid(row=3, column=2)
        self.E21param2 = Label(frame, textvariable=self.E21param2String,font=(self.font, "12"))
        self.E21param2.grid(row=4, column=2)
        self.E21param3 = Label(frame, textvariable=self.E21param3String,font=(self.font, "12"))
        self.E21param3.grid(row=5, column=2)

        self.dropdownE22Current = StringVar()
        self.E22param1String = StringVar()
        self.E22param2String = StringVar()
        self.E22param3String = StringVar()
        self.dropdownE22Current.set(self.effects[0])
        self.dropdownE22 = OptionMenu(frame, self.dropdownE22Current, *self.effects, command = optionmenuE22_selection)
        self.dropdownE22.grid(row=2, column=5,sticky="ew")
        self.E22param1 = Label(frame, textvariable=self.E22param1String,font=(self.font, "12"))
        self.E22param1.grid(row=3, column=5)
        self.E22param2 = Label(frame, textvariable=self.E22param2String,font=(self.font, "12"))
        self.E22param2.grid(row=4, column=5)
        self.E22param3 = Label(frame, textvariable=self.E22param3String,font=(self.font, "12"))
        self.E22param3.grid(row=5, column=5)

        self.dropdownE23Current = StringVar()
        self.E23param1String = StringVar()
        self.E23param2String = StringVar()
        self.E23param3String = StringVar()
        self.dropdownE23Current.set(self.effects[0])
        self.dropdownE23 = OptionMenu(frame, self.dropdownE23Current, *self.effects, command = optionmenuE23_selection)
        self.dropdownE23.grid(row=2, column=8,sticky="ew")
        self.E23param1 = Label(frame, textvariable=self.E23param1String,font=(self.font, "12"))
        self.E23param1.grid(row=3, column=8)
        self.E23param2 = Label(frame, textvariable=self.E23param2String,font=(self.font, "12"))
        self.E23param2.grid(row=4, column=8)
        self.E23param3 = Label(frame, textvariable=self.E23param3String,font=(self.font, "12"))
        self.E23param3.grid(row=5, column=8)

        self.G1BrightnesValue = StringVar()
        self.G1ShutterValue = StringVar()
        self.G1FadeValue = StringVar()
        self.G1Brightnes = Label(frame, textvariable=self.G1BrightnesValue,font=(self.font, "12"))
        self.G1Brightnes.grid(row=6, column=0)
        self.G1Shutter = Label(frame, textvariable=self.G1ShutterValue,font=(self.font, "12"))
        self.G1Shutter.grid(row=7, column=0)
        self.G1SFade = Label(frame, textvariable=self.G1FadeValue,font=(self.font, "12"))
        self.G1SFade.grid(row=8, column=0)


        self.G2BrightnesValue = StringVar()
        self.G2ShutterValue = StringVar()
        self.G2FadeValue = StringVar()
        self.G2Brightnes = Label(frame, textvariable=self.G2BrightnesValue,font=(self.font, "12"))
        self.G2Brightnes.grid(row=6, column=3)
        self.G2Shutter = Label(frame, textvariable=self.G2ShutterValue,font=(self.font, "12"))
        self.G2Shutter.grid(row=7, column=3)
        self.G2SFade = Label(frame, textvariable=self.G2FadeValue,font=(self.font, "12"))
        self.G2SFade.grid(row=8, column=3)

        self.G3BrightnesValue = StringVar()
        self.G3ShutterValue = StringVar()
        self.G3FadeValue = StringVar()
        self.G3Brightnes = Label(frame, textvariable=self.G3BrightnesValue,font=(self.font, "12"))
        self.G3Brightnes.grid(row=6, column=6)
        self.G3Shutter = Label(frame, textvariable=self.G3ShutterValue,font=(self.font, "12"))
        self.G3Shutter.grid(row=7, column=6)
        self.G2SFade = Label(frame, textvariable=self.G3FadeValue,font=(self.font, "12"))
        self.G2SFade.grid(row=8, column=6)

# L3D-Functions
    def startsending(self):
        self.do_send_rgb = True
        self.send_data_rgb()

    def stopsending(self):
        self.do_send_rgb = False

    def apply_manipulation(self, step):
        self.cubeWorld.control(MidiKey,MidiValue)
        paramValues = self.cubeWorld.getParamsAndValues()
        genValues = self.cubeWorld.getBrightnessAndShutterspeed()
        masterValues = self.cubeWorld.getMasterParams()
        #self.switchMidiButtonLights(MidiKey)
        #print(self.dmx.read(605))

        self.BrightnesValue.set(masterValues[0]+":"+str(round(masterValues[1],2)))
        self.ShutterValue.set(masterValues[2]+":"+str(round(masterValues[3],2)))

        self.G1param1String.set(paramValues[0][0]+':'+str(paramValues[0][1]))
        self.G1param2String.set(paramValues[0][2]+':'+str(paramValues[0][3]))
        self.G1param3String.set(paramValues[0][4]+':'+str(paramValues[0][5]))
        self.G1FadeValue.set(genValues[12]+":"+str(round(genValues[13],2)))

        self.G2param1String.set(paramValues[3][0]+':'+str(paramValues[3][1]))
        self.G2param2String.set(paramValues[3][2]+':'+str(paramValues[3][3]))
        self.G2param3String.set(paramValues[3][4]+':'+str(paramValues[3][5]))
        self.G2FadeValue.set(genValues[14]+":"+str(round(genValues[15],2)))

        self.G3param1String.set(paramValues[6][0]+':'+str(paramValues[6][1]))
        self.G3param2String.set(paramValues[6][2]+':'+str(paramValues[6][3]))
        self.G3param3String.set(paramValues[6][4]+':'+str(paramValues[6][5]))
        self.G3FadeValue.set(genValues[16]+":"+str(round(genValues[17],2)))

        self.E11param1String.set(paramValues[1][0]+':'+str(paramValues[1][1]))
        self.E11param2String.set(paramValues[1][2]+':'+str(paramValues[1][3]))
        self.E11param3String.set(paramValues[1][4]+':'+str(paramValues[1][5]))

        self.E12param1String.set(paramValues[4][0]+':'+str(paramValues[4][1]))
        self.E12param2String.set(paramValues[4][2]+':'+str(paramValues[4][3]))
        self.E12param3String.set(paramValues[4][4]+':'+str(paramValues[4][5]))

        self.E13param1String.set(paramValues[7][0]+':'+str(paramValues[7][1]))
        self.E13param2String.set(paramValues[7][2]+':'+str(paramValues[7][3]))
        self.E13param3String.set(paramValues[7][4]+':'+str(paramValues[7][5]))

        self.E21param1String.set(paramValues[2][0]+':'+str(paramValues[2][1]))
        self.E21param2String.set(paramValues[2][2]+':'+str(paramValues[2][3]))
        self.E21param3String.set(paramValues[2][4]+':'+str(paramValues[2][5]))

        self.E22param1String.set(paramValues[5][0]+':'+str(paramValues[5][1]))
        self.E22param2String.set(paramValues[5][2]+':'+str(paramValues[5][3]))
        self.E22param3String.set(paramValues[5][4]+':'+str(paramValues[5][5]))

        self.E23param1String.set(paramValues[8][0]+':'+str(paramValues[8][1]))
        self.E23param2String.set(paramValues[8][2]+':'+str(paramValues[8][3]))
        self.E23param3String.set(paramValues[8][4]+':'+str(paramValues[8][5]))

        self.G1BrightnesValue.set(genValues[0]+':'+str(round(genValues[1],2)))
        self.G2BrightnesValue.set(genValues[2]+':'+str(round(genValues[3],2)))
        self.G3BrightnesValue.set(genValues[4]+':'+str(round(genValues[5],2)))

        self.G1ShutterValue.set(genValues[6]+':'+str(genValues[7]))
        self.G2ShutterValue.set(genValues[8]+':'+str(genValues[9]))
        self.G3ShutterValue.set(genValues[10]+':'+str(genValues[11]))

        self.cubeWorld.update(step)

    def send_data_rgb(self):
        send_list = []
        if self.do_send_rgb:
            # compute animation
            self.apply_manipulation(self.framecount)
            # Package that shit with a nice header
            send_list.append(int(66))  # B
            send_list.append(int(69))  # E
            send_list.append(int(69))  # E
            send_list.append(int(70))  # F
            send_list.append(int(self.hSpeed))    # SPEED
            send_list.append(int(self.hBright))   # BRIGHT
            send_list.append(int(self.hPalMode))  # PalMODE
            send_list.append(int(self.hPal))      # Pal Select
            send_list.append(int(self.hRGBMode))  # RGB Mode ON

            # this sleep is stupid, we need another solution!
            time.sleep(0.015)
            send_list.extend(self.cubeWorld.get_cubedata())
            package = bytearray(send_list)

            self.framecount += 1
            # send the fuckin package
            self.con.write(package)
            self.after(self.sendSpeed, self.send_data_rgb)

    def checkbox_callback(self):
        self.cubeWorld.setArtnetControl(bool(self.artnet_switch.get()))

    def checkbox_color_callback(self):
        self.cubeWorld.setArtnetColorControl(bool(self.artnet_color_switch.get()))

    # def switchMidiButtonLights(self,Key):
    #     print(Key)
    #     if Key in [1,4,7,10,13,16,19,22,3,6,9,12,15,18,21,24]:
    #
    #         #self.MidiButtonListBool[key] is not self.MidiButtonListBool[key]
    #
    #         print('blub')
    #
    #     if(Key in [1,4,7,10,13,16,19,22,3,6,9,12,15,18,21,24]):
    #         if (self.MidiButtonListBool[Key]):
    #             midiout.send_message([0x90,int(Key),0x00])
    #             self.MidiButtonListBool[Key]=False
    #         else:
    #             midiout.send_message([0x90,int(Key),0x7E])
    #             self.MidiButtonListBool[Key]=True
    #

# -----------------------------------------
# midi routines


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        # output = message
        # print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        # print(message[1],message[2])
        global MidiKey
        MidiKey = message[1]
        global MidiValue
        MidiValue = message[2]

# -----------------------------------------

if __name__ == "__main__":
    print("\n =L3D-C0ntr0l=\n")

    print("Initialize MIDI CONTROL")
    port_a = 1
    port_b = 2
    midiin_a, portname_in_a = open_midiinput(port_a)
    midiin_b, portname_in_b = open_midiinput(port_b)
    #midiout, portname_out = open_midioutput(port)
    midiin_a.set_callback(MidiInputHandler(portname_in_a))
    midiin_b.set_callback(MidiInputHandler(portname_in_b))

    # print('Testing audio...')
    #
    # RATE = 44100
    # BUFFER = 882
    #
    # p = pyaudio.PyAudio()
    #
    # stream = p.open(
    #     format = pyaudio.paFloat32,
    #     channels = 1,
    #     rate = RATE,
    #     input = True,
    #     output = False,
    #     frames_per_buffer = BUFFER
    # )


    print("Starting main.")
    # midi ready

    root = App()
    root.title("=L3D-C0ntr0l= - - - Build : 1337.420")
    root.mainloop()
