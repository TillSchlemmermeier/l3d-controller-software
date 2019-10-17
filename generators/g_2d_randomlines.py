# modules
import numpy as np
from random import randint


class g_2d_randomlines():

    def __init__(self):
        self.blub0 = 0

    def control(self, blub0, blub1, blub2):
        self.blub0 = blub0

    def label(self):
        return ['empty','empty','empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 40, 10])
        world = np.zeros([3, 10, 10, 10])

        direction = randint(0, 1)
        if direction == 0:
            world[:, :, randint(0, 9)] = 1
        elif direction == 1:
            world[:, randint(0, 39), :] = 1

        # now we have to convert it
        world[:, 0, :, :] = world_2d[:, :10, :]
        world[:, 1, :, :] = world_2d[:, 10:20, :]
        world[:, 2, :, :] = world_2d[:, 20:30, :]
        world[:, 3, :, :] = world_2d[:, 30:40, :]

        return np.clip(world, 0, 1)
