# modules
import numpy as np
from scipy.ndimage.interpolation import rotate


class e_rotating_black_white():

    def __init__(self):

        # initial rotating parameters
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.step = 0
        self.broad = 0.1

        # create gradient
        self.colorworld = np.zeros([3, 10, 10, 10])

        # for i in range(10):
        #     self.colorworld[:, i, :, :] = (i/9.0)**2
        for i in range(10):
            self.colorworld[:, i, :, :] = 1/(1+np.exp((i-4.5)))

#        self.colorworld[0, :, :, :] *= self.color['r']
#        self.colorworld[0, :, :, :] *= self.color['g']
#        self.colorworld[0, :, :, :] *= self.color['b']

    def return_state(self):
        return [
            ['X speed', 'xspeed', round(self.xspeed,1)],
            ['Y speed', 'yspeed', round(self.yspeed,1)],
            ['Z speed', 'zspeed', round(self.zspeed,1)],
            ['broadening', 'broad', round(self.broad, 1)],
        ]

    def __call__(self, world, args):
		# === PARAMETERS START ===
        self.xspeed = args[0]*15+0.01
        self.yspeed = args[1]*15
        self.zspeed = args[2]*15
        self.broad = args[3]
        # === PARAMETERS END ===

        if self.broad == 0:
            for i in range(10):
                self.colorworld[:, i, :, :] = (i/9.0)**2

        else:
            for i in range(10):
                self.colorworld[:, i, :, :] = 1/(1+np.exp((i-4.0)/self.broad))


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
