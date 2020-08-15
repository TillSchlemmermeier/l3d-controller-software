# modules
import numpy as np
from scipy.signal import sawtooth

class g_planes():
    '''
    Generator: random

    Moves planes through the cube
    '''
    def __init__(self):
        print(' initializing g_planes')
        self.speed = 10
        self.dir = 1
        self.type = 0
        self.step = 0

        self.dict = {0: 'x, oscillating',
                     2: 'y, oscillating',
                     4: 'z, oscillating',
                     1: 'x, one-way',
                     3: 'y, one-way',
                     5: 'z, one-way'}

    #Strings for GUI
    def return_values(self):
        return [b'planes', b'speed', b'direction', b'saw/tri', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), str(self.dir), str(self.type), ''),'utf-8')


    def __call__(self, args):
        # parsing input
        self.speed = args[0]*10+0.5
        self.dir = int(round(args[1]*3))
        if args[2] > 0.5:
            self.type = 0.5
        else:
            self.type = 1.0

        # calculate frame
        world = np.zeros([3, 10, 10, 10])

        position = int(round((sawtooth(0.1*self.step*self.speed, self.type)+1)*4.51))

        if self.dir == 0:
            world[:, position,:,:] = 1.0
        elif self.dir == 1:
            world[:, :, position,:] = 1.0
        else:
            world[:, :,:,position] = 1.0

        self.step += 1
        return world
