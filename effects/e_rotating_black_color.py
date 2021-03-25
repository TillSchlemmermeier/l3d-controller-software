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

#        self.colorworld[0, :, :, :] *= self.color['r']
#        self.colorworld[0, :, :, :] *= self.color['g']
#        self.colorworld[0, :, :, :] *= self.color['b']


    #strings for GUI
    def return_values(self):
        return [b'rotating_black_color', b'X speed', b'Y speed', b'Z speed', b'R G B']

    def return_gui_values(self):
        RGBvalues = str(round(self.color[0]*10)) + ' ' + str(round(self.color[1]*10)) + ' ' + str(round(self.color[2]*10))

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.xspeed,1)), str(round(self.yspeed,1)), str(round(self.zspeed,1)), RGBvalues), 'utf-8')


    def __call__(self, world, args):
		# parse input
        self.xspeed = args[0]*15+0.01
        self.yspeed = args[1]*15
        self.zspeed = args[2]*15
        self.hue = args[3]

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
