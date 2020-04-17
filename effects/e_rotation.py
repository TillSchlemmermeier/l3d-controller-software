# modules
import numpy as np
from scipy.ndimage.interpolation import rotate

class e_rotation():

    def __init__(self):
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
		self.step = 0

    def return_values(self):
		pass

    def __call__(self, world, args):
		self.xspeed = 10*args[0]
		self.yspeed = 10*args[1]
		self.zspeed = 10*args[2]

        # create world
        # world = np.zeros([3, 10, 10, 10])

        # rotate
        world = rotate(world, step*self.xspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        world = rotate(world, step*self.yspeed,
                          axes = (0,1), order = 1,
	                      mode = 'nearest', reshape = False)

        world = rotate(world, step*self.zspeed,
                          axes = (0,2), order = 1,
	                      mode = 'nearest', reshape = False)

        # path world together
        # world[0, :, :, :] = newworld
        # world[1, :, :, :] = newworld
        # world[2, :, :, :] = newworld

        return np.clip(world, 0, 1)
