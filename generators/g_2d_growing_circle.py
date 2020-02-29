# modules
import numpy as np
from random import randint
from generators.convert2d import convert2d
from generators.circle2d import circle2d
from scipy.signal import sawtooth

class g_2d_growing_circle():

    def __init__(self, test = False, dim = [20, 10]):
        self.maxsize = 5
        self.growspeed = 1
        self.oscillate = 0
        self.dim = dim
        self.test = test

    def label(self):
        return ['maxsize',round(self.maxsize,2),'growspeed',round(self.growspeed,2),'osci, ex, im',round(self.oscillate,2)]

    def control(self, maxsize, growspeed, oscillate):
        self.maxsize = round(maxsize*20,2)
        self.growspeed = round(growspeed,2)
        self.oscillate = round(oscillate,2)

    def generate(self, step, dumpworld):

        world2d = np.zeros([3, self.dim[0], self.dim[1]])

        # oscillates between 0 and 1
        if self.oscillate < 0.3:
            osci = np.sin(step*self.growspeed)*0.5 + 1
        elif self.oscillate > 0.7:
            osci = sawtooth(step*self.growspeed, 0)*0.5 + 1
        else:
            osci = sawtooth(step*self.growspeed)*0.5 + 1

        # scales to maxsize
        size = self.maxsize * osci
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
