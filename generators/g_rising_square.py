# modules
import numpy as np
from random import randint, uniform

class g_rising_square():
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
        self.pause = 2
        self.random = 0
        self.flatworld = np.zeros([3, 4,10,10])
        self.step = 0

    #Strings for GUI
    def return_values(self):
        return [b'rising_square', b'speed', b'random', b'pause', b'']

    def __call__(self, args):
        self.speed = 7-int((args[0]*6))
        self.random = int(round(args[1]))
        self.pause = int(round(args[2]*40)+1)

#    def generate(self, step, dumpworld):
        world = np.zeros([3,10,10,10])

        if self.step % self.pause == 0:
            if self.random == 0:
                for i in range(self.nled):
                    self.flatworld[:, :, 9, :] = 1.0
            else:
                for i in range(self.nled):
                    self.flatworld[0, :, 9, :] = uniform(0,1)
                    self.flatworld[1, :, 9, :] = uniform(0,1)
                    self.flatworld[2, :, 9, :] = uniform(0,1)

        world[:, :, :, 0] = self.flatworld[:, 0, :, :]
        world[:, :, 9, :] = self.flatworld[:, 1, :, :]
        world[:, :, :, 9] = self.flatworld[:, 2, :, :]
        world[:, :, 0, :] = self.flatworld[:, 3, :, :]


        if self.step % self.speed == 0:
            self.flatworld = np.roll(self.flatworld, shift = -1, axis = 2)
            self.flatworld[:, :, 9, :] = 0.0
        self.step += 1
        return np.clip(world, 0, 1)
