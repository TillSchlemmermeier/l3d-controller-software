# modules
import numpy as np
from random import randint, uniform
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory

class g_random():
    '''
    Generator: random

    Random LED goes on

    Parameters:
    - Number of LEDs to turn on each cycle
    - Number of calls before new cycle
    - Random color for each cycle / each lamp
    - s2l Trigger On / Off
    '''
    def __init__(self):
        self.number_of_leds = 1
        self.counter = 1
        self.reset = 1
        self.lastvalue = 0
        self.randomcolor = 0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

        self.safeworld = np.zeros([3, 10, 10, 10])

    def return_values(self):
        return [b'g_random', b'N LED', b'Wait', b'Color', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel < 0:
            channel = 'noS2L'
        else:
            channel = 'Trigger'

        if self.randomcolor == 0:
            color = 'off'
        else:
            color = 'on'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number_of_leds,2)), str(round(self.reset,2)), color, channel),'utf-8')


    def __call__(self, args):
        self.number_of_leds = int((args[0])*20)
        self.reset = int(args[1]*10+1)
        self.randomcolor = int(round(args[2]))
        self.channel = int(args[3]*5)-1

        world = np.zeros([3, 10, 10, 10])

        # check if s2l is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.number_of_leds = int(current_volume*30)

        elif self.channel == 4 :
            current_volume = int(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = self.reset
            else:
                self.number_of_leds = 0


        if self.counter % self.reset == 0:
            if self.randomcolor == 0:
                for led in range(self.number_of_leds):
                    world[:, randint(0,9), randint(0,9), randint(0,9)] = 1.0
            else:
                color = hsv_to_rgb(uniform(0, 1), 1, 1)
                for led in range(self.number_of_leds):
                    world[:, randint(0,9), randint(0,9), randint(0,9)] = 1.0
                    for i in range(3):
                        world[i, :, :, :] *= color[i]

        else:
            world = self.safeworld

        self.safeworld = world

        if self.channel < 4:
            self.counter += 1
        else:
            self.counter = 0

        return world
