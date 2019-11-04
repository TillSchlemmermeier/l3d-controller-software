# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d

class g_2d_portal():

    def __init__(self):
        self.number = 1
        self.lastworld = np.zeros([3, 20, 40])


    def control(self, number, speed, direction):
        self.number = int(number*9)+1

    def label(self):
        return ['Number',self.number,'empty','empty','empty','empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, 20, 40])

        # move to the sides
        left = np.roll(self.lastworld, axis = 2, shift= -1)
        right = np.roll(self.lastworld, axis = 2, shift= 1)

        left[:, :, 19:] = 0.0
        right[:, :, :21] = 0.0

        for i in range(self.number):
            world_2d[:, randint(0,9), 19] = 1.0
            world_2d[:, randint(0,9), 20] = 1.0

#            world_2d[:, 4, 19] = 1.0
#            world_2d[:, 5, 20] = 1.0


        world_2d[:,:,:] += right[:, :, :]
        world_2d[:,:,:] += left[:, :, :]
        self.lastworld[:,:,:] = world_2d[:,:,:]

        # convert it to 2d
        world = convert2d(world_2d)

        return np.clip(world, 0, 1)
