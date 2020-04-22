# modules
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
from random import random, uniform

class e_prod_saturation():
    '''
    '''

    def __init__(self):

        self.c1 = 0.0
        self.distance = 0.0

    def control(self, c1, c2, balance):
        self.c1 = c1
        self.distance = c2

    def label(self):
        return ['c1',round(self.c1,2),'distance', round(self.distance,2),'empty','empty']

    def generate(self, step, world):

        color = hsv_to_rgb(self.c1,self.distance+random()*self.distance,1.0)

        world[0,:,:,:] *= color[0]
        world[1,:,:,:] *= color[1]
        world[2,:,:,:] *= color[2]

        return np.clip(world,0,1)
