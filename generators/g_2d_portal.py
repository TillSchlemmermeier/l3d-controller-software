# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d

class g_2d_portal():

    def __init__(self, test = False, dim = [20, 10] ):
        self.number = 1
        self.dim = dim
        self.lastworld = np.zeros([3, dim[0], dim[1]])
        self.test = test


    def control(self, number, speed, direction):
        self.number = int(number*9)+1

    def label(self):
        return ['Number',self.number,'empty','empty','empty','empty']

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, self.dim[0], self.dim[1]])

        # move to the sides
        left = np.roll(self.lastworld, axis = 1, shift= -1)
        right = np.roll(self.lastworld, axis = 1, shift= 1)

        # delete everything half part
        left[:, int(self.dim[0]/2)-1:, :] = 0.0
        right[:, :int(self.dim[0]/2)+1, :] = 0.0

        # turn on new leds
        for i in range(self.number):
            # left
            world_2d[:, int(self.dim[0]/2)-1, randint(0, self.dim[1]-1)] = 1.0
            # right
            world_2d[:, int(self.dim[0]/2), randint(0, self.dim[1]-1)] = 1.0

        # patch together worlds
        world_2d[:,:,:] += right[:, :, :]
        world_2d[:,:,:] += left[:, :, :]
        self.lastworld[:,:,:] = world_2d[:,:,:]

        if not self.test:
            # convert it to 2d
            world = convert2d(world_2d)
        else:
            world = world_2d

        return np.clip(world, 0, 1)
