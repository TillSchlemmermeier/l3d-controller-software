import numpy as np
from generators.convert2d import convert2d
from random import uniform

class g_2d_column():
    def __init__(self, test = False, dim = [60, 10]):
        self.dim = dim
        self.test = test
        self.amplitude = 1.0

    def control(self, *args):
        self.amplitude = args[0]*2

    def label(self):
        return ['ampli',round(self.amplitude,2), 'empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):
        # generate empty world
        world = np.zeros([3, self.dim[0], self.dim[1]])

        for i in range(29):
            world[:, i, :] = i/30.0
            world[:, -i, :] = i/30.0

        world = world ** self.amplitude
        world -= uniform(0,1)

        if not self.test:
            # convert it to 2d
            world3d = convert2d(world)
        else:
            world3d = world

        return world3d
