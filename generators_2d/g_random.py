# modules
import numpy as np
from random import randint

class g_random():
    '''
    Generator: random
    '''
    def __init__(self, resolution):
        print(' initialize g_random')
        self.number_of_leds = 1
        self.counter = 1
        self.reset = 1
        self.resolution = resolution
        self.safeworld = np.zeros([3, resolution[0], resolution[1]])

    def return_values(self):
        return [b'g_random', b'N LED', b'Wait', b'',b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number_of_leds,2)), str(round(self.reset,2)), '', ''),'utf-8')


    def __call__(self, args):
        self.number_of_leds = int((args[0])*20)
        self.reset = int(args[1]*10+1)

        world = np.zeros([3, resolution[0], resolution[1]])

        if self.counter % self.reset == 0:
            for led in range(self.number_of_leds):
                world[:, randint(0,self.resolution[0]), randint(0,self.resolution[1])] = 1.0
        else:
            world = self.safeworld

        self.safeworld = world
        self.counter += 1
        return world
