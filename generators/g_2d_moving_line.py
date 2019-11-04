# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d

class g_2d_random():

    def __init__(self):
        self.blub0 = 0

    def control(self, number, blub1, blub2):
        self.number = number

    def label(self):
        return ['Number',self.number,'empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 20, 40])

        for i in self.number:
            world_2d[:, randint(0,19), randint(0,39)]
        # now we have to convert it
        world = convert2d(world_2d)

        return np.clip(world, 0, 1)
