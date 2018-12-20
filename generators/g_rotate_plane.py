# modules
import numpy as np
from scipy.ndimage.interpolation import rotate

class g_rotate_plane():
    def __init__(self):
        self.original = np.zeros([10,10,10])
        for i in range(8):
            self.original[4:5, 1:-1, 1:-1] = 1

        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0

    def control(self, xspeed, yspeed, zspeed):
        self.xspeed = 10*xspeed+0.01
        self.yspeed = 10*yspeed
        self.zspeed = 10*zspeed


    def label(self):
        return ['rotating speed 1', round(self.xspeed, 2),
                'rotating speed 2', round(self.yspeed, 2),
                'rotating speed 3', round(self.zspeed, 2)]


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

        newworld = rotate(newworld, step*self.zspeed,
                          axes = (0,2), order = 1,
	                      mode = 'nearest', reshape = False)


        # insert array
        world[0, :, :, :] = newworld
        world[1, :, :, :] = newworld
        world[2, :, :, :] = newworld

        return np.clip(world, 0, 1)
