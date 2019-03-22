# modules
import numpy as np
from random import randint


class g_randomlines():

    def __init__(self):
        self.blub0 = 0

    def return_values(self):
        pass

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.blub0 = args[0]

        world = np.zeros([3, 10, 10, 10])

        direction = randint(0, 2)
        if direction == 0:
            world[:, :, randint(0, 9), randint(0, 9)] = 1

        elif direction == 1:
            world[:, randint(0, 9), :, randint(0, 9)] = 1
        elif direction == 2:
            world[:, randint(0, 9), randint(0, 9), :] = 1

        return np.clip(world, 0, 1)
