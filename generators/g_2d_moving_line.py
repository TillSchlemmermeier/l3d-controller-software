# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d

class g_2d_moving_line():

    def __init__(self):
        self.direction = 'right'
        self.counter = 0

    def control(self, *args):
        if round(args[0]) > 0:
            self.direction = 'left'
        else:
            self.direction = 'right'

    def label(self):
        return ['Direction',self.direction,'empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 20, 40])

        # draw lines
        if self.direction == 'right':
            world_2d[:, :, self.counter] = 1.0
        else:
            world_2d[:, :, 39-self.counter] = 1.0

        # take care of counter
        self.counter += 1
        if self.counter > 39:
            self.counter = 0

        # now we have to convert it
        world = convert2d(world_2d)

        return np.clip(world, 0, 1)
