# modules
import numpy as np
from colorsys import hsv_to_rgb
from scipy.ndimage.interpolation import rotate


class e_rotating_black_color():


    def __init__(self):

        # initial rotating parameters
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.color = [0.1,0.0,0.0]
        self.step = 0
        self.hue = 0.1

        # create gradient
        self.colorworld = np.zeros([3, 10, 10, 10])

        for i in range(10):
            self.colorworld[:, i, :, :] = (i/9.0)**2


    def return_state(self):
        return [
            ['X speed', 'xspeed', round(self.xspeed,1)],
            ['Y speed', 'yspeed', round(self.yspeed,1)],
            ['Z speed', 'zspeed', round(self.zspeed,1)],
            ['R G B', 'hue', str(round(self.color[0]*10)) + ' ' + str(round(self.color[1]*10)) + ' ' + str(round(self.color[2]*10))],
        ]
    
    def __call__(self, world, args):
		# === PARAMETERS START ===
        self.xspeed = args[0]*15+0.01
        self.yspeed = args[1]*15
        self.zspeed = args[2]*15
        self.hue = args[3]
        # === PARAMETERS END ===

        self.color = hsv_to_rgb(self.hue, 1, 1)

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

        self.step += 1

        for i in range(3):
            newworld[i, :, :, :] = newworld[i, :, :, :]*self.color[i]

        world = newworld * world

        return np.clip(world, 0, 1)
