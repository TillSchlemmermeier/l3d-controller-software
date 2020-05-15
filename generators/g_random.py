# modules
import numpy as np
from random import randint

class g_random():
    '''
    Generator: random
    '''
    def __init__(self):
        print(' initialize g_random')
        self.number_of_leds = 1

    def return_values(self):
        return [b'g_random', b'Number of LEDs', b'', b'',b'']

    def __call__(self, args):
        self.number_of_leds = int((args[0])*20)

        world = np.zeros([3, 10, 10, 10])

        for led in range(self.number_of_leds):
            world[:, randint(0,9), randint(0,9), randint(0,9)] = 1.0

        return world
