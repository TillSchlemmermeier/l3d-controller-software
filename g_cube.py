# modules
import numpy as np
from cube_utils import *
from random import uniform, randint
from scipy.signal import sawtooth


class g_cube():

    def __init__(self):
        self.size = 2

    def control(size, blub0, blub1):
        self.size = round(size*4)

    def generate(self, step):

        world = np.zeros([3,10,10,10])

        tempworld = np.zeros([10,10,10])
        tempworld[:, :, :] = 0.0
        size = self.size
        # write cube
        # x slices
        tempworld[4-size, 4-size:6+size, 4-size:6+size] += 1
        tempworld[5+size, 4-size:6+size, 4-size:6+size] += 1
        # y slices
        tempworld[4-size:6+size, 4-size, 4-size:6+size] += 1
        tempworld[4-size:6+size, 5+size, 4-size:6+size] += 1
        # z slices
        tempworld[4-size:6+size, 4-size:6+size, 4-size] += 1
        tempworld[4-size:6+size, 4-size:6+size, 5+size] += 1

        world[0,:,:,:] = tempworld
        world[1,:,:,:] = tempworld
        world[2,:,:,:] = tempworld


        return np.clip(world,0,1)
