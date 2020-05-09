# modules
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
from random import random, uniform

class e_prod_hue():
    '''
    '''

    def __init__(self):

        self.c1 = 0.0
        self.distance = 0.2

    #strings for GUI
    def return_values(self):
        return [b'prod_hue', b'Color', b'distance', b'', b'']

    def __call__(self, world, args):
        # parsing input
        self.c1 = args[0]
        self.distance = args[1]

        color = hsv_to_rgb(self.c1+uniform(-0.5,0.5)*self.distance,1.0,1.0)

        world[0,:,:,:] *= color[0]
        world[1,:,:,:] *= color[1]
        world[2,:,:,:] *= color[2]

        return world
