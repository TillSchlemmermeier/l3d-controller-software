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

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

        self.safeworld = np.zeros([3, 10, 10, 10])

    def return_state(self):
        return [
            ['N LED', 'number_of_leds', round(self.number_of_leds,2)],
            ['Wait', 'reset', round(self.reset,2)],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.number_of_leds = int((args[0])*20)
        self.reset = int(args[1]*10+1)
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][round(args[2]*5)]
        # === PARAMETERS END ===

        world = np.zeros([3, 10, 10, 10])

        # check if s2l is activated
        if isinstance(self.channel, int):
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.number_of_leds = int(current_volume*30)

        elif self.channel == 'Trigger' :
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = self.reset
            else:
                self.number_of_leds = 0


        if self.counter % self.reset == 0:
            for led in range(self.number_of_leds):
                world[:, randint(0,9), randint(0,9), randint(0,9)] = 1.0

        else:
            world = self.safeworld

        self.safeworld = world

        if self.channel != 'Trigger':
            self.counter += 1
        else:
            self.counter = 0

        return world
