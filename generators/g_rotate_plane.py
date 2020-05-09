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
        self.step = 0

    #Strings for GUI
    def return_values(self):
        return [b'rotate_plane', b'xspeed', b'yspeed', b'zspeed', b'']

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.xspeed = 10*args[0]+0.01
        self.yspeed = 10*args[1]
        self.zspeed = 10*args[2]

        # create world
        world = np.zeros([3, 10, 10, 10])

        # rotate
        newworld = rotate(self.original, self.step*self.xspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.yspeed,
                          axes = (0,1), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.zspeed,
                          axes = (0,2), order = 1,
	                      mode = 'nearest', reshape = False)


        # insert array
        world[0, :, :, :] = newworld
        world[1, :, :, :] = newworld
        world[2, :, :, :] = newworld

        self.step += 1

        return np.clip(world, 0, 1)
