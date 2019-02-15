# modules
import numpy as np
from scipy.signal import sawtooth

class g_planes():
    '''
    Generator: random

    Moves planes through the cube
    '''
    def __init__(self):
        self.speed = 10
        self.dir = 1
        self.type = 0

        self.dict = {0: 'x, oscillating',
                     1: 'x, one-way',
                     2: 'y, oscillating',
                     3: 'y, one-way',
                     4: 'z, oscillating',
                     5: 'z, one-way'}

    def return_values(self):
        return {'Movement Speed': [self.speed, 10, ''],
                'Direction':, [self.dir, 6, self.dict[self.dir]]}

    def __call__(self, args):
        # parsing input
        self.speed = int((args[0]+1)*10)
        self.dir = int(round(args[1]*6))

        # calculate frame
        world = np.zeros([3, 10, 10, 10])
        if self.dir % 2 == 0:
            type = 0.5  # triangle wave
        else:
            type = 1    # rising ramp

        position = int(round((sawtooth(0.1*step*self.speed, type)+1)*4.51))

        if self.dir == 0:
            world[:, position,:,:] = 1.0
        elif self.dir == 1:
            world[:, :, position,:] = 1.0
        else:
            world[:, :,:,position] = 1.0

        return world
