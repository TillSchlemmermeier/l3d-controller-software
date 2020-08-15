# modules
import numpy as np
from scipy.ndimage.interpolation import rotate

class e_rotation():

    def __init__(self):
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.step = 0

    #strings for GUI
    def return_values(self):
        return [b'rotation', b'X speed', b'Y speed', b'Z speed', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.xspeed,1)), str(round(self.yspeed,1)), str(round(self.zspeed,1)), '', 'utf-8')

    def __call__(self, world, args):
        self.xspeed = 10*args[0]
        self.yspeed = 10*args[1]
        self.zspeed = 10*args[2]

        # create world
        # world = np.zeros([3, 10, 10, 10])

        # rotate
        for i in range(3):

            world[i, :, :, :] = rotate(world[i, :, :, :], self.step*self.xspeed,
                              axes = (1,2), order = 1,
    	                      mode = 'nearest', reshape = False)

            world[i, :, :, :] = rotate(world[i, :, :, :], self.step*self.yspeed,
                              axes = (0,1), order = 1,
    	                      mode = 'nearest', reshape = False)

            world[i, :, :, :] = rotate(world[i, :, :, :], self.step*self.zspeed,
                              axes = (0,2), order = 1,
    	                      mode = 'nearest', reshape = False)

        # path world together
        # world[0, :, :, :] = newworld
        # world[1, :, :, :] = newworld
        # world[2, :, :, :] = newworld
        world[:, :, :, :] = world[:, :, :, :]**1.3
        self.step += 1
        return np.clip(world, 0, 1)
