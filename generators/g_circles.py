# modules
import numpy as np
from random import randint

class g_circles():
    '''
    Generator: kreise halt
    '''

    def __init__(self):
        self.size = 2
        self.sides = False

        self.frames = []

        # size 4
        self.size4 = np.zeros([10,10])

        # straight
        self.size4[1,3:7] = 1.0
        self.size4[8,3:7] = 1.0
        self.size4[3:7,1] = 1.0
        self.size4[3:7,8] = 1.0

        # diag
        self.size4[2,2] = 1.0
        self.size4[2,7] = 1.0
        self.size4[7,2] = 1.0
        self.size4[7,7] = 1.0

        # size 3
        self.size3 = np.zeros([10,10])

        # straight
        self.size3[2,3:7] = 1.0
        self.size3[7,3:7] = 1.0
        self.size3[3:7,2] = 1.0
        self.size3[3:7,7] = 1.0

        # size 2
        self.size2 = np.zeros([10,10])

        # straight
        self.size2[3,4:6] = 1.0
        self.size2[6,4:6] = 1.0
        self.size2[4:6,3] = 1.0
        self.size2[4:6,6] = 1.0

    def control(self, blub0, blub2, blub1):
        pass

    def label(self):
        return ['empty','empty','empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])
        world[:, randint(0,9), :, :] = self.size2
        world[:, randint(0,9), :, :] = self.size3
        world[:, randint(0,9), :, :] = self.size4
        return np.clip(world, 0, 1)
