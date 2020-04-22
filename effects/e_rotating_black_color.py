# modules
import numpy as np
from scipy.ndimage.interpolation import rotate


class e_rotating_black_color():


    def __init__(self):

        # initial rotating parameters
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.color = {'r':1.0, 'g':0.0, 'b':0.0}
        self.step = 0

        # create gradient
        self.colorworld = np.zeros([3, 10, 10, 10])

        for i in range(10):
            self.colorworld[:, i, :, :] = (i/9.0)**2

#        self.colorworld[0, :, :, :] *= self.color['r']
#        self.colorworld[0, :, :, :] *= self.color['g']
#        self.colorworld[0, :, :, :] *= self.color['b']


    def return_values(self):
        return [['', ''],
				['', ''],
                ['', ''],
				['', '']]


    def __call__(self, world, args):
		# parse input
        self.xspeed = args[0]*15+0.01
        self.yspeed = args[1]*15
        self.zspeed = args[2]*15
        self.color = color_translate(args[3])

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


        #self.colorworld[0, :, :, :] *= self.color['r']
        #self.colorworld[0, :, :, :] *= self.color['g']
        #self.colorworld[0, :, :, :] *= self.color['b']

        newworld[0, :, :, :] = newworld[0, :, :, :]*self.color['r']
        newworld[1, :, :, :] = newworld[1, :, :, :]*self.color['g']
        newworld[2, :, :, :] = newworld[2, :, :, :]*self.color['b']

        world = newworld * world

        self.step += 1

        return np.clip(world, 0, 1)



def color_translate(value):
    value *= 127
    #translates values from 0 to 127 to rgb values
    if (value>126):
        value=126

    r_out = 0.0
    g_out = 0.0
    b_out = 0.0

    if(value<=21):
        r_out=1
        g_out=value/21.0
        b_out=0
    elif(value>21 and value<=42):
        r_out=1-((value-21.0)/21.0)
        g_out=1
        b_out=0
    elif(value>42 and value<=63):
        r_out=0
        g_out=1
        b_out=(value-42.0)/21.0
    elif(value>63 and value<=84):
        r_out=0
        g_out=1-((value-63.0)/21.0)
        b_out=1
    elif(value>84 and value<=105):
        r_out=(value-84.0)/21.0
        g_out=0
        b_out=1
    elif(value>105):
        r_out=1
        g_out=0
        b_out=1-((value-105.0)/21.0)

    return {'r':r_out, 'g':g_out, 'b':b_out}
