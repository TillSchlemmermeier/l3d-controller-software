# modules
import numpy as np
from random import randint
from convert2d import convert2d

class g_2d_randomlines():

    def __init__(self):
        self.blub0 = 0

    def control(self, blub0, blub1, blub2):
        self.blub0 = blub0

    def label(self):
        return ['empty','empty','empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 20, 40])
        world = np.zeros([3, 10, 10, 10])

        direction = randint(0, 1)
        if direction == 0:
            world_2d[:, :, randint(0, 39)] = 1
        elif direction == 1:
            world_2d[:, randint(0, 19), :] = 1

        # now we have to convert it
        world = convert2d(world_2d)

        return np.clip(world, 0, 1)
