# modules
import numpy as np
from scipy.ndimage.interpolation import rotate


class e_rotating_rainbow():

    def __init__(self):

        # initial rotating parameters
        self.speed = 0
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.1
        self.step = 1

    #strings for GUI
    def return_values(self):
        return [b'rotating_rainbow', b'Rainbow_speed', b'X speed', b'Y speed', b'Z speed']


    def __call__(self, world, args):
		# parse input
        self.speed = args[0]*10
        self.xspeed = args[1]*15+0.01
        self.yspeed = args[2]*15
        self.zspeed = args[3]*15

        # create gradient
        self.rainbowworld = np.zeros([3, 10, 10, 10])

        for i in range(10):
            self.rainbowworld[0, i, :, :] = color_translate(int(round((i*12.7 + self.step * self.speed)%127)))[0]
            self.rainbowworld[1, i, :, :] = color_translate(int(round((i*12.7 + self.step * self.speed)%127)))[1]
            self.rainbowworld[2, i, :, :] = color_translate(int(round((i*12.7 + self.step * self.speed)%127)))[2]


        # rotate
        newworld = rotate(self.rainbowworld, self.step*self.xspeed,
                          axes = (1,2), order = 1,
                          mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.yspeed,
                          axes = (1,3), order = 1,
                          mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.zspeed,
                          axes = (2,3), order = 1,
                          mode = 'nearest', reshape = False)

        world *= newworld
        self.step += 1

        return np.clip(world, 0, 1)


def color_translate(value):
    #value *= 127
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

    return [r_out, g_out, b_out]
