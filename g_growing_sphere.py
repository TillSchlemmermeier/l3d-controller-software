# modules
import numpy as np
# from cube_utils import *
from scipy.signal import sawtooth


class g_growing_sphere():
    '''
    Generator: growing_sphere

    a growing hollow sphere in the middle of the cube

    Parameters:
    - maxsize
    - growspeed
    - oscillate y/n
    '''

    def __init__(self):
        self.maxsize = 10
        self.growspeed = 1
        self.oscillate = 0

    def control(self, maxsize, growspeed, oscillate):
        self.maxsize = maxsize*10
        self.growspeed = growspeed
        self.oscillate = oscillate

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])

        # oscillates between 0 and 1
        if self.oscillate < 0.5:
            osci = np.sin(step*self.growspeed)*0.5 + 2
        else:
            osci = sawtooth(step*self.growspeed)*0.5 + 2

        # scales to maxsize
        size = self.maxsize * osci
        # creates hollow sphere with parameters
        world[0, :, :, :] = hsphere(size)
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        return world


def hsphere(radius):

    world = np.zeros([10, 10, 10])

    for x in range(10):
        for y in range(10):
            for z in range(10):
                dist = np.sqrt((x-4.5)**2+(y-4.5)**2+(z-4.5)**2)
                world[x, y, z] = 1.0/(radius-dist+0.0001)**7

    return np.round(np.clip(world, 0, 1), 3)
