import numpy as np
from scipy.signal import sawtooth

class g_squares():

    def __init__(self):
        self.speed = 10
        self.dir = 1
        self.type = 0

    def control(self, speed, dir, type):
        self.speed = int(speed*9)
        self.dir = int(round(dir*3))
        self.type = type

    def label(self):
        return ['speed',round(self.speed,2),'direction', self.dir,'osc/down/up', round(self.type,1)]

    def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])
        if self.type < 0.33:
            position = int( round((np.sin(0.1*step*self.speed)+1)*4.5))
        elif self.type >= 0.33 and self.type < 0.66:
            position = int( round((sawtooth(0.1*step*self.speed)+1)*4.5))
        else:
            position = int( round((sawtooth(0.1*step*self.speed, width=0)+1)*4.5))

        if self.dir == 0:
            world[:, position,:,:] = 1.0
            world[:, :, 1:-1, 1:-1] = 0.0
        elif self.dir == 1:
            world[:, :, position,:] = 1.0
            world[:, 1:-1, :, 1:-1] = 0.0
        else:
            world[:, :,:,position] = 1.0
            world[:, 1:-1, 1:-1, :] = 0.0


        return world
