# modules
import numpy as np
from random import choice
from generators.g_cut import g_cut
from generators.g_squares import g_squares
from generators.g_blank import g_blank

class a_squares_cut():
    '''
    Automat: lines
    '''

    def __init__(self):
        self.counter = 0

        # counter for changes
        self.square_start = 500
        self.square_dimm = 0.01
        self.brightness = 1.0

        # initialize generator
        self.generator1 = g_squares()
        self.generator1.control(9,0,0.1)

        self.generator2 = g_cut()
        self.generator2.control(1,0,0)

    def control(self, square_start, dimm, blub1):
        self.square_start = int(300*square_start)
        self.square_dimm = dimm*0.1+0.001

    def label(self):
        return ['count fade', 'empty',
                'empty', 'empty',
                'empty', 'empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        # cuts
        world[:, :, :, :] = self.generator2.generate(self.counter, 0)

        # cuts
        if self.counter > self.square_start and self.counter%2 == 0:
            self.brightness -= self.square_dimm
            world += self.brightness * self.generator1.generate(self.counter ,0)

        # squares
        if self.brightness <= 0.0:
            self.counter = 0
            self.brightness = 1.0

        self.counter += 1

        return np.clip(world, 0, 1)
