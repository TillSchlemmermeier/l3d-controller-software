# modules
import numpy as np
# from cube_utils import *
from scipy.signal import sawtooth


class g_planes_falling():
    '''
    Generator: planes


    '''

    def __init__(self):
        self.speed = 10
        self.dir = 1
        self.step = 0

    #Strings for GUI
    def return_values(self):
        return [b'planes_falling', b'speed', b'direction x/y/z', b'', b'']

    def __call__(self, args):
        self.speed = int(args[0]*9)
        self.dir = int(round(args[1]*3))

    #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])
        position = int( round((sawtooth(0.1*self.step*self.speed)+1)*4.5))

        if self.dir == 0:
            world[:, position,:,:] = 1.0
        elif self.dir == 1:
            world[:, :, position,:] = 1.0
        else:
            world[:, :,:,position] = 1.0
        self.step += 1
        return world
