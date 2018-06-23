# modules
import numpy as np
# from cube_utils import *
# from scipy.signal import sawtooth


class g_planes():
    '''
    Generator: planes


    '''

    def __init__(self):
        self.speed = 10
        self.dir = 1

    def control(self, speed, dir, dump):
        self.speed = int(speed*9)
        self.dir = int(round(dir*3))

    def label(self):
        return ['speed',round(self.speed,2),'direction', self.dir,'empty','empty']

    def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])
        position = int( round((np.sin(0.1*step*self.speed)+1)*4.5))

        if self.dir == 0:
            world[:, position,:,:] = 1.0
        elif self.dir == 1:
            world[:, :, position,:] = 1.0
        else:
            world[:, :,:,position] = 1.0

        return world
