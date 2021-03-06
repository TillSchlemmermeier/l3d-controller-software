# modules
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb

class e_gradient():
    '''
    '''

    def __init__(self):

        self.c1 = [0.1,0.0,0.0]
        self.c2 = [0.4,0.4,0.0]
        self.balance = 1.0

    def control(self, c1, c2, balance):
        self.c1 = c1 # hsv_to_rgb(c1,1,1)
        self.c2 = c2 # hsv_to_rgb(c2,1,1)
        self.balance = balance*2

        if self.c2 > self.c1:
            temp = self.c1
            self.c1 = self.c2
            self.c2 = temp

    def label(self):
        return ['c1',self.c1,'c2', self.c2,'balance',self.balance]

    def generate(self, step, world):

        # generate color list
        x = np.array([0,1,2,3,4,5,6,7,8,9])
        y = self.sigmoid(x-4.5)*(self.c1-self.c2)+self.c2

        # choose color according to x position
        for x in range(10):
            color = hsv_to_rgb(y[x],1,1)
            world[0,x,:,:] = world[0,x,:,:] * color[0]
            world[1,x,:,:] = world[1,x,:,:] * color[1]
            world[2,x,:,:] = world[2,x,:,:] * color[2]

        return np.clip(world,0,1)


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x[:]*self.balance))
