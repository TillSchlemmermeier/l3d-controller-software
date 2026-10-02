# modules
import numpy as np
from scipy.ndimage.interpolation import rotate

class g_rotating_circle():
    '''
    Generator: kreise halt
    '''

    def __init__(self):
        self.counter = 0

        self.xspeed = 0
        self.yspeed = 1.0
        self.zspeed = 0
        self.brightness = 0.5

    def return_state(self):
        return [
            ['xpseed', 'xspeed', round(self.xspeed,2)],
            ['yspeed', 'yspeed', round(self.yspeed,2)],
            ['zspeed', 'zspeed', round(self.zspeed,2)],
            ['brightness', 'brightness', round(self.brightness,2)],
        ]

    def __call__(self, args):
#       # === PARAMETERS START ===
        self.xspeed = args[0]*2
        self.yspeed = args[1]*2
        self.zspeed = args[2]*2
        self.brightness = args[3]*0.5+0.5
        # === PARAMETERS END ===

        # create world
        world1 = np.zeros([3, 10, 10, 10])
        world2 = np.zeros([3, 10, 10, 10])

        world2[:, 2, 4, 2] = self.brightness
        world2[:, 2, 5, 2] = self.brightness
        world2[:, 7, 4, 7] = self.brightness
        world2[:, 7, 5, 7] = self.brightness
        world2[:, 4, 2, 4] = self.brightness
        world2[:, 4, 7, 4] = self.brightness
        world2[:, 5, 2, 5] = self.brightness
        world2[:, 5, 7, 5] = self.brightness
        world2[:, 3, 3, 3] = self.brightness
        world2[:, 3, 6, 3] = self.brightness
        world2[:, 6, 3, 6] = self.brightness
        world2[:, 6, 6, 6] = self.brightness


        # rotate
        for i in range(3):
            world2[i, :, :, :] = rotate(world2[i, :, :, :], self.counter*self.xspeed,
                              axes = (1,2), order = 1,
    	                      mode = 'nearest', reshape = False)

            world2[i, :, :, :] = rotate(world2[i, :, :, :], self.counter*self.yspeed,
                              axes = (0,1), order = 1,
    	                      mode = 'nearest', reshape = False)

            world2[i, :, :, :] = rotate(world2[i, :, :, :], self.counter*self.zspeed,
                              axes = (0,2), order = 1,
    	                      mode = 'nearest', reshape = False)


        world1[:, 2, 4, 2] = self.brightness
        world1[:, 2, 5, 2] = self.brightness
        world1[:, 7, 4, 7] = self.brightness
        world1[:, 7, 5, 7] = self.brightness
        world1[:, 4, 2, 4] = self.brightness
        world1[:, 4, 7, 4] = self.brightness
        world1[:, 5, 2, 5] = self.brightness
        world1[:, 5, 7, 5] = self.brightness
        world1[:, 3, 3, 3] = self.brightness
        world1[:, 3, 6, 3] = self.brightness
        world1[:, 6, 3, 6] = self.brightness
        world1[:, 6, 6, 6] = self.brightness

        self.counter += 1

        return np.clip(world1+world2, 0, 1)
