# modules
import numpy as np
from colorsys import hsv_to_rgb
from scipy.ndimage.interpolation import rotate

class e_rotating_rainbow():

    def __init__(self):

        # initial rotating parameters
        self.speed = 0
        self.rotation = 0.1
        self.gradient_length = 1.0
        self.step = 1
        self.rotX = 1
        self.rotYZ = 1

    #strings for GUI
    def return_values(self):
        return [b'rotating_rainbow', b'Length', b'Speed', b'Rot_X', b'Rot_YZ']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,1)), str(round(self.gradient_length,1)), str(round(self.rotX,1)), str(round(self.rotYZ,1))), 'utf-8')


    def __call__(self, world, args):
		# parse input
        self.speed = args[0]*0.1
        self.gradient_length = args[1]
        self.rotX = args[2]*15+0.01
        self.rotYZ = args[3]*15+0.01

        # create gradient
        self.rainbowworld = np.zeros([3, 10, 10, 10])

        for i in range(3):
            for j in range (10):
                self.rainbowworld[i, j, :, :] = hsv_to_rgb((j / 10) * self.gradient_length + self.step * self.speed, 1, 1)[i]

        # rotate
        newworld = rotate(self.rainbowworld, self.step*self.rotX,
                          axes = (1,2), order = 1,
                          mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.rotYZ,
                          axes = (1,3), order = 1,
                          mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.rotYZ,
                          axes = (2,3), order = 1,
                          mode = 'nearest', reshape = False)

        world *= newworld
        self.step += 1
        #if int(round((i*self.gradient_length + self.step * self.speed))) > 127:
        #    self.step = 0

        return np.clip(world, 0, 1)


    def color_translate(self, value):
        #value *= 127
        #translates values from 0 to 127 to rgb values
        #if value>127:
        #    value-=127
        value = value % 127
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

        return [r_out, g_out, b_out]
