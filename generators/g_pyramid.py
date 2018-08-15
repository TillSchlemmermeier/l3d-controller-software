# modules
import numpy as np
from scipy.signal import sawtooth

class g_pyramid():
    '''
    Generator: pyramid
    '''

    def __init__(self):
        self.size = 1
        self.speed = 0.2

    def control(self, size, speed, blub1):
        self.size = int(size+1.5)
        self.speed = speed

    def label(self):
        return ['size',round(self.size,2),'speed',round(self.speed,2),'empty','empty','empty','empty',]

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        # straight lines
        world[:,0,:,0] = 1.0
        world[:,0,0,:] = 1.0
        world[:,0,:,9] = 1.0
        world[:,0,9,:] = 1.0

        # diagonal random_lines
        for i in range(1,5):
            if self.size == 2:
                world[:,i*2,i,i] = 1.0
                world[:,i*2,9-i,i] = 1.0
                world[:,i*2,i,9-i] = 1.0
                world[:,i*2,9-i,9-i] = 1.0

                world[:,i*2+1,i,i] = 1.0
                world[:,i*2+1,9-i,i] = 1.0
                world[:,i*2+1,i,9-i] = 1.0
                world[:,i*2+1,9-i,9-i] = 1.0
            else:
                world[:,i,i,i] = 1.0
                world[:,i,9-i,i] = 1.0
                world[:,i,i,9-i] = 1.0
                world[:,i,9-i,9-i] = 1.0

        # brightness
        for x in range(10):
            world[:,x,:,:] *= sawtooth(self.speed*step+x, width = 1)

        return np.clip(world, 0, 1)
