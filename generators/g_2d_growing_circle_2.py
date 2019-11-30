# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d
from generators.circle2d import circle2d
from scipy.signal import sawtooth

class g_2d_growing_circle_2():

    def __init__(self, test = False, dim = [60, 10]):
        self.maxsize = 5
        self.minsize = 1
        self.speed = 0
        self.dim = dim
        self.test = test

    def label(self):
        return ['maxsize',round(self.maxsize,2),'growspeed',round(self.growspeed,2),'osci, ex, im',round(self.oscillate,2)]

    def control(self, maxsize, minsize, speed):
        self.maxsize = round(maxsize*20,2)
        self.minsize = round(minsize*20,2)
        self.speed = round(speed,2)

    def generate(self, step, dumpworld):

        world2d = np.zeros([3, self.dim[0], self.dim[1]])

        # calculate current radius
        size = (self.sawtooth(step*self.speed)+1)*0.5 * (self.maxsize - self.minsize) + self.minsize

        # creates hollow sphere with parameters
        world2d[0 , :, :] = circle2d(size, self.dim[0]/2-0.5, self.dim[1]/2-0.5)
        world2d[1:, :, :] = world2d[0, :, :]
        world2d[2:, :, :] = world2d[0, :, :]

        if not self.test:
            # convert it to 2d
            world = convert2d(world2d)
        else:
            world = world2d

        return np.clip(world, 0, 1)
