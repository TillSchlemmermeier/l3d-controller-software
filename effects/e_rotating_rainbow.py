# modules
import numpy as np
from scipy.ndimage.interpolation import rotate


class e_rotating_rainbow():

    def __init__(self):

        # initial rotating parameters
        self.speed = 0
        self.rotation = 0.1
        self.gradient_length = 1.0
        self.black_length = 1.0
        self.step = 1

    #strings for GUI
    def return_values(self):
        return [b'rotating_rainbow', b'Rainbow Speed', b'Rotation Speed', b'Gradient length', b'Black length']


    def __call__(self, world, args):
		# parse input
        self.speed = args[0]*10
        self.rotation = args[1]*15+0.01
        self.gradient_length = args[2]*12.7
        self.black_length = int(args[3]*10)

        # create gradient
        self.rainbowworld = np.zeros([3, 10, 10, 10])

        for i in range(10):
            self.rainbowworld[0, i, :, :] = self.color_translate(int(round((i*self.gradient_length + self.step * self.speed))))[0]
            self.rainbowworld[1, i, :, :] = self.color_translate(int(round((i*self.gradient_length + self.step * self.speed))))[1]
            self.rainbowworld[2, i, :, :] = self.color_translate(int(round((i*self.gradient_length + self.step * self.speed))))[2]


        # rotate
        newworld = rotate(self.rainbowworld, self.step*self.rotation,
                          axes = (1,2), order = 1,
                          mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.rotation,
                          axes = (1,3), order = 1,
                          mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.rotation,
                          axes = (2,3), order = 1,
                          mode = 'nearest', reshape = False)

        world *= newworld
        self.step += 1
        if self.step >= 127 + self.black_length:
            self.step = 0

        return np.clip(world, 0, 1)


    def color_translate(self, value):
        #value *= 127
        #translates values from 0 to 127 to rgb values
        if (value>127+self.black_length):
            value=127+self.black_length

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
        elif(value>105 and value <=127):
            r_out=1
            g_out=0
            b_out=1-((value-105.0)/21.0)
        elif(value>127):
            r_out=1-((value-127)/self.black_length)
            g_out=0
            b_out=0

        return [r_out, g_out, b_out]
