# modules
import numpy as np
from random import randint, uniform

class g_rising_square():
    '''
    Generator: cube

    a cube in the cube

    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    '''

    def __init__(self):
        self.nled = 1
        self.speed = 2
        self.pause = 2
        self.random = 0
        self.flatworld = np.zeros([3, 4,10,10])
        self.step = 0

    #Strings for GUI
    def return_values(self):
        return [b'rising_square', b'speed', b'Col On/Off', b'pause', b'']

    def __call__(self, args):
        self.speed = 7-int((args[0]*6))
        self.random = int(round(args[1]))
        self.pause = int(round((args[2]+0.06)*40)+1)

#    def generate(self, step, dumpworld):
        world = np.zeros([3,10,10,10])

        if self.step % self.pause == 0:
            if self.random == 0:
                for i in range(self.nled):
                    self.flatworld[:, :, 9, :] = 1.0
            else:
                for i in range(self.nled):
                    color = color_translate(uniform(0,127))
                    self.flatworld[0, :, 9, :] = color[0]
                    self.flatworld[1, :, 9, :] = color[1]
                    self.flatworld[2, :, 9, :] = color[2]

        world[:, :, :, 0] = self.flatworld[:, 0, :, :]
        world[:, :, 9, :] = self.flatworld[:, 1, :, :]
        world[:, :, :, 9] = self.flatworld[:, 2, :, :]
        world[:, :, 0, :] = self.flatworld[:, 3, :, :]


        if self.step % self.speed == 0:
            self.flatworld = np.roll(self.flatworld, shift = -1, axis = 2)
            self.flatworld[:, :, 9, :] = 0.0
        self.step += 1
        return np.clip(world, 0, 1)


def color_translate(value):
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
