#! /usr/bin/python3.5

from Tkinter import *
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


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        frame = Frame(self)
        frame.pack()

        # CONECTION
        try:
            self.con = serial.Serial('/dev/ttyACM0', 230400)
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
        self.framecount = 0
        self.send_array_rgb = []
        # self.send_list =[]

        self.generators = ["NONE", " g_cube", "g_random", "g_growing_sphere"]
        self.effects = ["NONE", "blur"]
        # Header Information
        self.hSpeed = 1
        self.hBright = 200
        self.hPa = 1
        self.hPalMode = 0
        self.hRGBMode = 1

        self.send_array_rgb = bytearray(3009)

        # GUI Callabcks
        def optionmenuG1_selection(event):
            self.cubeWorld.set_Genenerator("A", self.dropdownG1Current.get())
            pass

        def optionmenuG2_selection(event):
            self.cubeWorld.set_Genenerator("B", self.dropdownG2Current.get())
            pass

        def optionmenuE1_selection(event):
            # EFFEKT
            pass

        def optionmenuE2_selection(event):
            # EffEKT
            pass

        # GUI Elements
        self.startButton = Button(frame, text="Start", command=self.startsending)
        self.startButton.grid(row=0, column=4)

        self.stopButton = Button(frame, text="Stop", command=self.stopsending)
        self.stopButton.grid(row=0, column=5)

        self.labelG1 = Label(frame, text="Generator 1")
        self.labelG1.grid(row=1, column=0)

        self.labelG2 = Label(frame, text="Generator 2")
        self.labelG2.grid(row=1, column=1)

        self.labelE1 = Label(frame, text="Effekt 1")
        self.labelE1.grid(row=1, column=2)

        self.labelE2 = Label(frame, text="Effekt 2")
        self.labelE2.grid(row=1, column=3)

        self.dropdownG1Current = StringVar()
        self.dropdownG1Current.set(self.generators[0])
        self.dropdownG1 = OptionMenu(frame, self.dropdownG1Current, *self.generators, command = optionmenuG1_selection)
        self.dropdownG1.grid(row=2, column=0)

        self.dropdownG2Current = StringVar()
        self.dropdownG2Current.set(self.generators[0])
        self.dropdownG2 = OptionMenu(frame, self.dropdownG2Current, *self.generators,command = optionmenuG2_selection)
        self.dropdownG2.grid(row=2, column=1)

        self.dropdownE1Current = StringVar()
        self.dropdownE1Current.set(self.effects[0])
        self.dropdownE1 = OptionMenu(frame, self.dropdownE1Current, *self.effects,command = optionmenuE1_selection)
        self.dropdownE1.grid(row=2, column=2)

        self.dropdownE2Current = StringVar()
        self.dropdownE2Current.set(self.effects[0])
        self.dropdownE2 = OptionMenu(frame, self.dropdownE2Current, *self.effects, command = optionmenuE2_selection)
        self.dropdownE2.grid(row=2, column=3)


# L3D-Functions
    def startsending(self):
        self.do_send_rgb = True
        self.send_data_rgb()

    def stopsending(self):
        self.do_send_rgb = False

    def apply_manipulation(self, step):
        self.cubeWorld.control(MidiKey,MidiValue)
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
    root.title("PyControll")
    root.mainloop()
