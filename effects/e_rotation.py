# modules
import numpy as np
from scipy.ndimage.interpolation import rotate

class e_rotation():

    def __init__(self):
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0

    def label(self):
        return ['x speed',round(self.xspeed, 2),'y speed', np.round(self.xspeed, 2),'z speed', np.round(self.yspeed, 2)]

    def control(self, xspeed, yspeed, zspeed):
        self.xspeed = 10*xspeed
        self.yspeed = 10*yspeed
        self.zspeed = 10*zspeed

    def generate(self, step, tempworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        # rotate
        tempworld = rotate(tempworld, step*self.xspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        tempworld = rotate(tempworld, step*self.yspeed,
                          axes = (0,1), order = 1,
	                      mode = 'nearest', reshape = False)

        tempworld = rotate(tempworld, step*self.zspeed,
                          axes = (0,2), order = 1,
	                      mode = 'nearest', reshape = False)

        # path world together
        world[0, :, :, :] = newworld
        world[1, :, :, :] = newworld
        world[2, :, :, :] = newworld

        return np.clip(tempworld, 0, 1)
