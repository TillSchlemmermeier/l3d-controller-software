# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d

class g_2d_rain():

    def __init__(self, test = False, dim = [60, 10]):
        self.number = 1
        self.wait   = 1
        self.dir    =-1
        self.dim = dim
        self.lastworld = np.zeros([3, dim[0], dim[1]])
        self.test = test


    def control(self, number, speed, direction):
        self.number = int(number*9)+1
        self.wait   = 10 - int(speed*9)

        if direction > 0.5:
            self.dir = -1
        else:
            self.dir =  1

    def label(self):
        return ['Number',self.number,'Speed', self.wait,'Up/Down',self.dir]

    def generate(self, step, dumpworld):

        world_2d = np.zeros([3, self.dim[0], self.dim[1]])
        self.lastworld = np.roll(self.lastworld, axis = 2, shift=-self.dir)

        # proces old world
        if self.dir == -1:
            self.lastworld[ :, :, 0]  = 0.0
        else:
            # up to down
            self.lastworld[ :, :, -1] = 0.0


        # proces old world
        if step % self.wait == 0:
            for i in range(self.number):
                if self.dir == -1:
                    pass
#                    self.lastworld[ :, 9, :] = 0.0
#                    self.lastworld[:, 10:, :] = 0.0
                    world_2d[:, randint(0, self.dim[0]-1), 0] = 1.0
                else:
                    # up to down
                    world_2d[:, randint(0, self.dim[0]-1), -1] = 1.0


        world_2d[:,:,:] += self.lastworld
        self.lastworld[:,:,:] = world_2d[:,:,:]

        if not self.test:
            # convert it to 2d
            world = convert2d(world_2d)
        else:
            world = world_2d

        return np.clip(world, 0, 1)
