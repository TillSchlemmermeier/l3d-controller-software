# modules
import numpy as np
from random import randint


class g_randomlines():

    def __init__(self):
        self.reset = 1
        self.counter = 0
        self.saveworld = np.zeros([3,10,10,10])


    #Strings for GUI
    def return_values(self):
        return [b'randomlines', b'wait', b'', b'', b'']

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.reset = int(args[0]*10)+1

        world = np.zeros([3, 10, 10, 10])

        if self.counter % self.reset == 0:

            direction = randint(0, 2)
            if direction == 0:
                world[:, :, randint(0, 9), randint(0, 9)] = 1

            elif direction == 1:
                world[:, randint(0, 9), :, randint(0, 9)] = 1
            elif direction == 2:
                world[:, randint(0, 9), randint(0, 9), :] = 1
        else:
            world = self.saveworld

        self.counter += 1

        self.saveworld = world
        return np.clip(world, 0, 1)
