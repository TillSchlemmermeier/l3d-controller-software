import numpy as np
from generators.convert2d import convert2d
from random import uniform

class g_column():
    def __init__(self, test = False, dim = [10, 10, 10]):
        self.dim = dim
        self.test = test
        self.amplitude = 0.5
        self.direction = 1

    def control(self, *args):
        self.amplitude = args[0]+0.5
        self.direction = args[1]-0.5

    def label(self):
        return ['ampli',round(self.amplitude,2), 'empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):
        # generate empty world
        world = np.zeros([3, 10, 10, 10])

        for i in range(10):
            if self.direction > 0:
                world[:, i, :, :] = i/30.0
            else:
                world[:, 9-i, :, :] = i/30.0

        world = np.clip(world,0,1)
        world = world ** self.amplitude
        world -= uniform(0,1)

        return np.clip(world,0,1)
