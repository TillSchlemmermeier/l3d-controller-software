# modules
import numpy as np
from random import randint


class g_random():
    '''
    Generator: random

    Turns on random LEDs with a random color

    Parameters:
    - number: Number of LEDs to turned on per call
    '''

    def __init__(self):
        self.number = 1

    def control(self, number, blub0, blub1):
        self.number = int((number*20)+1)  # +1 makes sure that minimum number is > 0

    def label(self):
        return ['number',self.number,'empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):
        # create the world
        world = np.zeros([3, 10, 10, 10])

        for i in range(self.number):
            world[:, randint(0, 9), randint(0, 9), randint(0, 9)] = 1.0

        return world
