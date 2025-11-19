# modules
import numpy as np
from scipy.ndimage.interpolation import rotate


class e_rotating_fade():

    def __init__(self):

        # initial rotating parameters
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.step = 0
        self.amount = 0

        self.fadeworld = np.zeros([3, 10, 10, 10])

        # create gradient
        self.colorworld = np.zeros([3, 10, 10, 10])

        for i in range(10):
            self.colorworld[:, i, :, :] = np.sqrt(i/9.0)

#        self.colorworld[0, :, :, :] *= self.color['r']
#        self.colorworld[0, :, :, :] *= self.color['g']
#        self.colorworld[0, :, :, :] *= self.color['b']

    def return_state(self):
        return [
            ['X speed', 'xspeed', round(self.xspeed,1)],
            ['Y speed', 'yspeed', round(self.yspeed,1)],
            ['Z speed', 'zspeed', round(self.zspeed,1)],
            ['amount', 'amount', round(self.amount,1)],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.xspeed = args[0]*15+0.01
        self.yspeed = args[1]*15
        self.zspeed = args[2]*15
        self.amount = args[3]
        # === PARAMETERS END ===

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


        world = self.fadeworld * newworld * self.amount + world

        self.step += 1
        self.fadeworld = np.clip(world, 0, 1)

        return np.clip(world, 0, 1)
