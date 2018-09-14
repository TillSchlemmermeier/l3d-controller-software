# modules
import numpy as np
from scipy.ndimage.interpolation import rotate

class g_silpion3():
    '''
    '''

    def __init__(self):
        self.original = np.zeros([10,10,10])
        for i in range(8):
            self.original[i+1, 4, 1:9-i] = 1

        self.xspeed = 0.1
        self.yspeed = 0.1

    def control(self, xspeed, yspeed, blub2):
        self.xspeed = 5*xspeed+0.01
        self.yspeed = 5*yspeed


    def label(self):
        return ['rotating speed 1', round(self.xspeed, 2),
                'rotating speed 2', round(self.yspeed, 2),
                'empty', 'empty']


    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        # rotate
        newworld = rotate(self.original, step*self.xspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, step*self.yspeed,
                          axes = (0,1), order = 1,
	                      mode = 'nearest', reshape = False)

        # insert array
        world[0, :, :, :] = newworld
        world[1, :, :, :] = newworld
        world[2, :, :, :] = newworld

        return np.clip(world, 0, 1)
