# modules
import numpy as np
from scipy.ndimage.interpolation import rotate


class e_rotating_black_blue():

    def __init__(self):

        # initial rotating parameters
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.step = 0

        # create gradient
        self.colorworld = np.zeros([3, 10, 10, 10])

        for i in range(10):
            self.colorworld[2, i, :, :] = (i/9.0)**2

    def control(self, xspeed, yspeed, zspeed):
        self.xspeed = 10*xspeed+0.01
        self.yspeed = 10*yspeed
        self.zspeed = 10*zspeed

    def label(self):
        return ['rotating speed 1', round(self.xspeed, 2),
                'rotating speed 2', round(self.yspeed, 2),
                'rotating speed 3', round(self.zspeed, 2)]

    def generate(self, step, world):

        # rotate
        newworld = rotate(self.colorworld, self.step*self.xspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.yspeed,
                          axes = (1,3), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.zspeed,
                          axes = (2,3), order = 1,
	                      mode = 'nearest', reshape = False)


        world = newworld * world

        self.step += 1

        return np.clip(world, 0, 1)
