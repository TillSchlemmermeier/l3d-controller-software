# modules
import numpy as np
from random import randint

class g_trees():
    '''
    Generator: cube

    a cube in the cube

    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    '''

    def __init__(self):
        self.nled = 1
        self.speed = 2
        self.flatworld = np.zeros([4,10,10])

    def control(self, size, speed, blub1):
        self.nled = int(round(size*4)+1)
        self.speed = int((speed*4)+1)

    def label(self):
        return ['number of led',self.nled,'speed', self.speed,'empty','empty']

    def generate(self, step, dumpworld):
        world = np.zeros([3,10,10,10])


        for i in range(self.nled):
            self.flatworld[randint(0,3), 9, randint(0,9)] = 1.0

        world[0, :, :, 0] = self.flatworld[0, :, :]
        world[0, :, 9, :] = self.flatworld[1, :, :]
        world[0, :, :, 9] = self.flatworld[2, :, :]
        world[0, :, 0, :] = self.flatworld[3, :, :]

        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        if step % self.speed == 0:
            self.flatworld = np.roll(self.flatworld, shift = -1, axis = 1)
            self.flatworld = np.roll(self.flatworld, shift = randint(-1,1), axis = 2)

            self.flatworld[:, 9, :] = 0.0


        return np.clip(world, 0, 1)
