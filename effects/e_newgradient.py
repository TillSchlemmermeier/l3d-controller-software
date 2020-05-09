# modules
import numpy as np


class e_newgradient():
    '''
    Effect: redyellow

    '''

    def __init__(self):
        self.speed = 0.5
        self.c1 = {'r':1.0, 'g':0.0, 'b':0.0}
        self.c2 = {'r':0.0, 'g':0.0, 'b':1.0}
        self.step = 0

    #strings for GUI
    def return_values(self):
        return [b'newgradient', b'speed', b'Color 1', b'Color 2', b'']


    def control(self, speed, c1, c2):
        self.speed = speed*0.1
        self.c1 = color_translate(c1)
        self.c2 = color_translate(c2)


    def generate(self, step, world):


#        corr_red = 0.5*(np.mean(self.c1['r'] - self.c2['r']))
        corr_red = abs(self.c1['r'] - self.c2['r'])
        red = corr_red *(np.sin(self.speed*self.step))-([self.c1['r'], self.c2['r']].min()+1)

        corr_green = 0.5*(np.mean(self.c1['g'] - self.c2['g']))
        green = corr_green *(np.sin(self.speed*self.step) + 1)

        corr_blue = 0.5*(np.mean(self.c1['b'] - self.c2['b']))
        blue = corr_blue *(np.sin(self.speed*self.step) + 1)

        world[0, :, :, :] = world[0, :, :, :]*red
        world[1, :, :, :] = world[1, :, :, :]*green
        world[2, :, :, :] = world[2, :, :, :]*blue

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
