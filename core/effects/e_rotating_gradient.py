# modules
import numpy as np
from scipy.ndimage.interpolation import rotate
from colorsys import rgb_to_hsv, hsv_to_rgb


class e_rotating_gradient():

    def __init__(self):

        # initial rotating parameters
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.step = 0

        self.base_color = 0
        self.spread = 0.5

        # create gradient
        self.colorworld = np.zeros([3, 10, 10, 10])

        for i in range(10):
            self.colorworld[0, i, :, :] = i/9.0
            self.colorworld[1, i, :, :] = 1.0 - i/9.0
            self.colorworld[2, i, :, :] = 0.5*(1.0 - i/9.0)

#        self.colorworld[0, :, :, :] *= self.color['r']
#        self.colorworld[0, :, :, :] *= self.color['g']
#        self.colorworld[0, :, :, :] *= self.color['b']

    def return_state(self):
        return [
            ['base color', 'xspeed', round(self.xspeed,1)],
            ['spread', 'yspeed', round(self.yspeed,1)],
            ['Z speed', 'zspeed', round(self.zspeed,1)],
        ]

    def __call__(self, world, args):
		# parse input
        self.base_color = args[0]
        self.spread     = args[1]*0.5
        self.zspeed     = args[2]*15

        # calculate color
        color1 = hsv_to_rgb(self.base_color, 1, 1)
        color2 = hsv_to_rgb(self.base_color+self.spread, 1, 1)

        red   = np.linspace(color1[0], color2[0], 10)
        green = np.linspace(color1[1], color2[1], 10)
        blue  = np.linspace(color1[2], color2[2], 10)

        # color world
        for i in range(10):
            world[0, i, :, :] *= red[i]
            world[1, i, :, :] *= green[i]
            world[2, i, :, :] *= blue[i]


        # rotate
        newworld = rotate(self.colorworld, self.step*self.zspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        world = newworld * world

        self.step += 1

        return np.clip(world, 0, 1)
