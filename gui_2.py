#! /usr/bin/python3.5

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
from rtmidi.midiutil import open_midiinput
# from copy import deepcopy
from CubeWorld import CubeWorld
# from time import sleep
import time as time

MidiKey = 0
MidiValue = 0


# sound2light stuff ende

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        frame = Frame(self)
        frame.pack()

        # CONECTION
        try:
            self.con =  serial.Serial('/dev/ttyACM0', 230400)
            print(self.con)
        except IOError:
            self.con = serial.Serial('/dev/ttyACM1', 230400)
            print(self.con)

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

        self.generators = ["g_blank", " g_cube", "g_random", "g_growing_sphere","g_orbiter","g_randomlines",
                           "g_sphere", "g_snake","g_planes", "g_planes_falling", "g_corner", "g_corner_grow",
                            "g_shooting_star", "g_orbiter2"]
        self.effects = ["e_blank","e_fade2blue","e_rainbow","e_staticcolor", "e_violetblue", "e_redyellow"]
        # Header Information
        self.hSpeed = 1
        self.hBright = 200
        self.hPal = 1
        self.hPalMode = 0
        self.hRGBMode = 1

        self.send_array_rgb = bytearray(3009)

        # GUI Callabcks
        def optionmenuG1_selection(event):
            self.cubeWorld.set_Genenerator("A", self.dropdownG1Current.get(),0)
            pass

        def optionmenuG2_selection(event):
            self.cubeWorld.set_Genenerator("B", self.dropdownG2Current.get(),0)
            pass

        def optionmenuG3_selection(event):
            self.cubeWorld.set_Genenerator("C", self.dropdownG3Current.get(),0)
            pass

        def optionmenuE1_selection(event):
            self.cubeWorld.set_Genenerator("A", self.dropdownE1Current.get(),1)
            pass

        def optionmenuE2_selection(event):
            self.cubeWorld.set_Genenerator("B", self.dropdownE2Current.get(),1)
            pass

        def optionmenuE3_selection(event):
            self.cubeWorld.set_Genenerator("C", self.dropdownE3Current.get(),1)
            pass

        # GUI Elements
        self.startButton = Button(frame, text="Start", command=self.startsending)
        self.startButton.grid(row=0, column=4)

        self.stopButton = Button(frame, text="Stop", command=self.stopsending)
        self.stopButton.grid(row=0, column=5)

        self.labelG1 = Label(frame, text="Generator 1")
        self.labelG1.grid(row=1, column=0)

        self.labelG2 = Label(frame, text="Generator 2")
        self.labelG2.grid(row=1, column=2)

        self.labelG2 = Label(frame, text="Generator 3")
        self.labelG2.grid(row=1, column=4)

        self.labelE1 = Label(frame, text="Effekt 1")
        self.labelE1.grid(row=1, column=1)

        self.labelE2 = Label(frame, text="Effekt 2")
        self.labelE2.grid(row=1, column=3)

        self.labelE2 = Label(frame, text="Effekt 3")
        self.labelE2.grid(row=1, column=5)

        self.dropdownG1Current = StringVar()
        self.G1param1String = StringVar()
        self.G1param2String = StringVar()
        self.G1param3String = StringVar()
        self.dropdownG1Current.set(self.generators[0])
        self.dropdownG1 = OptionMenu(frame, self.dropdownG1Current, *self.generators, command = optionmenuG1_selection)
        self.dropdownG1.grid(row=2, column=0)
        self.G1param1 = Label(frame, textvariable=self.G1param1String)
        self.G1param1.grid(row=3, column=0)
        self.G1param2 = Label(frame, textvariable=self.G1param2String)
        self.G1param2.grid(row=4, column=0)
        self.G1param3 = Label(frame, textvariable=self.G1param3String)
        self.G1param3.grid(row=5, column=0)

        self.dropdownG2Current = StringVar()
        self.G2param1String = StringVar()
        self.G2param2String = StringVar()
        self.G2param3String = StringVar()
        self.dropdownG2Current.set(self.generators[0])
        self.dropdownG2 = OptionMenu(frame, self.dropdownG2Current, *self.generators,command = optionmenuG2_selection)
        self.dropdownG2.grid(row=2, column=2)
        self.G2param1 = Label(frame, textvariable=self.G2param1String)
        self.G2param1.grid(row=3, column=2)
        self.G2param2 = Label(frame, textvariable=self.G2param2String)
        self.G2param2.grid(row=4, column=2)
        self.G2param3 = Label(frame, textvariable=self.G2param3String)
        self.G2param3.grid(row=5, column=2)

        self.dropdownG3Current = StringVar()
        self.G3param1String = StringVar()
        self.G3param2String = StringVar()
        self.G3param3String = StringVar()
        self.dropdownG3Current.set(self.generators[0])
        self.dropdownG3 = OptionMenu(frame, self.dropdownG3Current, *self.generators,command = optionmenuG3_selection)
        self.dropdownG3.grid(row=2, column=4)
        self.G3param1 = Label(frame, textvariable=self.G3param1String)
        self.G3param1.grid(row=3, column=4)
        self.G3param2 = Label(frame, textvariable=self.G3param2String)
        self.G3param2.grid(row=4, column=4)
        self.G3param3 = Label(frame, textvariable=self.G3param3String)
        self.G3param3.grid(row=5, column=4)

        self.dropdownE1Current = StringVar()
        self.E1param1String = StringVar()
        self.E1param2String = StringVar()
        self.E1param3String = StringVar()
        self.dropdownE1Current.set(self.effects[0])
        self.dropdownE1 = OptionMenu(frame, self.dropdownE1Current, *self.effects,command = optionmenuE1_selection)
        self.dropdownE1.grid(row=2, column=1)
        self.E1param1 = Label(frame, textvariable=self.E1param1String)
        self.E1param1.grid(row=3, column=1)
        self.E1param2 = Label(frame, textvariable=self.E1param2String)
        self.E1param2.grid(row=4, column=1)
        self.E1param3 = Label(frame, textvariable=self.E1param3String)
        self.E1param3.grid(row=5, column=1)

        self.dropdownE2Current = StringVar()
        self.E2param1String = StringVar()
        self.E2param2String = StringVar()
        self.E2param3String = StringVar()
        self.dropdownE2Current.set(self.effects[0])
        self.dropdownE2 = OptionMenu(frame, self.dropdownE2Current, *self.effects, command = optionmenuE2_selection)
        self.dropdownE2.grid(row=2, column=3)
        self.E2param1 = Label(frame, textvariable=self.E2param1String)
        self.E2param1.grid(row=3, column=3)
        self.E2param2 = Label(frame, textvariable=self.E2param2String)
        self.E2param2.grid(row=4, column=3)
        self.E2param3 = Label(frame, textvariable=self.E2param3String)
        self.E2param3.grid(row=5, column=3)

        self.dropdownE3Current = StringVar()
        self.E3param1String = StringVar()
        self.E3param2String = StringVar()
        self.E3param3String = StringVar()
        self.dropdownE3Current.set(self.effects[0])
        self.dropdownE3 = OptionMenu(frame, self.dropdownE3Current, *self.effects, command = optionmenuE3_selection)
        self.dropdownE3.grid(row=2, column=5)
        self.E3param1 = Label(frame, textvariable=self.E3param1String)
        self.E3param1.grid(row=3, column=5)
        self.E3param2 = Label(frame, textvariable=self.E3param2String)
        self.E3param2.grid(row=4, column=5)
        self.E3param3 = Label(frame, textvariable=self.E3param3String)
        self.E3param3.grid(row=5, column=5)


# L3D-Functions
    def startsending(self):
        self.do_send_rgb = True
        self.send_data_rgb()

    def stopsending(self):
        self.do_send_rgb = False

    def apply_manipulation(self, step):
        self.cubeWorld.control(MidiKey,MidiValue)
        paramValues = self.cubeWorld.getParamsAndValues()

        self.G1param1String.set(paramValues[0][0]+':'+str(paramValues[0][1]))
        self.G1param2String.set(paramValues[0][2]+':'+str(paramValues[0][3]))
        self.G1param3String.set(paramValues[0][4]+':'+str(paramValues[0][5]))

        self.G2param1String.set(paramValues[2][0]+':'+str(paramValues[2][1]))
        self.G2param2String.set(paramValues[2][2]+':'+str(paramValues[2][3]))
        self.G2param3String.set(paramValues[2][4]+':'+str(paramValues[2][5]))

        self.G3param1String.set(paramValues[4][0]+':'+str(paramValues[4][1]))
        self.G3param2String.set(paramValues[4][2]+':'+str(paramValues[4][3]))
        self.G3param3String.set(paramValues[4][4]+':'+str(paramValues[4][5]))

        self.E1param1String.set(paramValues[1][0]+':'+str(paramValues[1][1]))
        self.E1param2String.set(paramValues[1][2]+':'+str(paramValues[1][3]))
        self.E1param3String.set(paramValues[1][4]+':'+str(paramValues[1][5]))

        self.E2param1String.set(paramValues[3][0]+':'+str(paramValues[3][1]))
        self.E2param2String.set(paramValues[3][2]+':'+str(paramValues[3][3]))
        self.E2param3String.set(paramValues[3][4]+':'+str(paramValues[3][5]))

        self.E3param1String.set(paramValues[5][0]+':'+str(paramValues[5][1]))
        self.E3param2String.set(paramValues[5][2]+':'+str(paramValues[5][3]))
        self.E3param3String.set(paramValues[5][4]+':'+str(paramValues[5][5]))


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
            time.sleep(0.01)
            send_list.extend(self.cubeWorld.get_cubedata())
            blub = bytearray(send_list)

            self.framecount += 1
            # send the fuckin package
            self.con.write(blub)
            self.after(self.sendSpeed, self.send_data_rgb)
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

    # Initialize MIDI INPUT
    port = 1
    # try:
    midiin, port_name = open_midiinput(port)
    # except (EOFError, KeyboardInterrupt):
    #    sys.exit()

    print("Attaching MIDI input callback handler.")
    midiin.set_callback(MidiInputHandler(port_name))

    print("Starting main.")
    # midi ready

    root = App()
    root.title("l3d-controll - - - Build : 1337.420")
    root.mainloop()
