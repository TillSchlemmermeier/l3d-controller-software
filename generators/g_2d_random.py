# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d

class g_2d_random():

    def __init__(self, test = False, dim = [20, 10]):
        self.number = 1
        self.dim = dim
        self.test = test

    def control(self, *args):
        self.number = int(args[0]*9)+1

    def label(self):
        return ['Number',self.number,'empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, self.dim[0], self.dim[1]])

        for i in range(self.number):
            world_2d[:, randint(0,self.dim[0]-1), randint(0,self.dim[1]-1)] = 1

        if not self.test:
            # convert it to 2d
            world = convert2d(world_2d)
        else:
            world = world_2d

        return np.clip(world, 0, 1)
