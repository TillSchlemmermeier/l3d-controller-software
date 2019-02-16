# modules
import numpy as np
from random import randint

class g_random():
    '''
    Generator: random
    '''
    def __init__(self):
        self.number_of_leds = 1
        pass

    def return_values():
        pass#return {'Number of LEDs', self.number_of_leds}

    def __call__(self, args):
        self.number_of_leds = int((args[0]+1)*10)

        world = np.zeros([3, 10, 10, 10])

        for led in range(self.number_of_leds):
            world[:, randint(0,9), randint(0,9), randint(0,9)] = 1.0

        return world
