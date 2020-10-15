# modules
import numpy as np
from random import randint
from multiprocessing import shared_memory

class g_random():
    '''
    Generator: random
    '''
    def __init__(self):
        print(' initialize g_random')
        self.number_of_leds = 1
        self.counter = 1
        self.reset = 1

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

        self.safeworld = np.zeros([3, 10, 10, 10])

    def return_values(self):
        return [b'g_random', b'N LED', b'Wait', b'channel',b'']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number_of_leds,2)), str(round(self.reset,2)), channel, ''),'utf-8')


    def __call__(self, args):
        self.number_of_leds = int((args[0])*20)
        self.reset = int(args[1]*10+1)
        self.channel = int(args[2]*4)-1

        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.number_of_leds += current_volume*30


        world = np.zeros([3, 10, 10, 10])
        if self.counter % self.reset == 0:
            for led in range(self.number_of_leds):
                world[:, randint(0,9), randint(0,9), randint(0,9)] = 1.0
        else:
            world = self.safeworld

        self.safeworld = world
        self.counter += 1
        return world
