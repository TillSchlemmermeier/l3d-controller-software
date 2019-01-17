# modules
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere
from random import randint

# fortran routine is in g_growing_sphere_f.f90

class g_darksphere():
    '''
    Generator: growing_sphere

    a growing hollow sphere in the middle of the cube

    Parameters:
    - maxsize
    - growspeed
    - oscillate y/n
    '''

    def __init__(self):
        self.maxsize = 10
        self.growspeed = 1
        self.nled = 10
        self.oscillate = 0
        self.lastworld = np.zeros([3,10,10,10])

    def label(self):
        return ['maxsize',round(self.maxsize,2),'growspeed',round(self.growspeed,2),'number of leds', self.nled]

    def control(self, maxsize, growspeed, oscillate):
        self.maxsize = maxsize*10
        self.growspeed = growspeed
        self.nled = int(oscillate*20)+1

    def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])
        for i in range(self.nled):
            world[:, randint(0,9), randint(0,9), randint(0,9)] = 1.0

        world += self.lastworld*0.9
        self.lastworld = world

        osci = sawtooth(step*self.growspeed*0.5)*0.5 + 1

        # scales to maxsize
        size = 5 * osci
        # creates hollow sphere with parameters
        darkworld = np.clip(gen_hsphere(size, 5.5, 5.5, 5.5),0,1)

        # darkworld = np.zeros([10,10,10])

        # darkworld[:,5:,:] = 0.5

        world[0, :, :, :] -= darkworld[:, :, :]
        world[1, :, :, :] -= darkworld[:, :, :]
        world[2, :, :, :] -= darkworld[:, :, :]

        #self.lastworld = world

        return np.round(np.clip(world, 0, 1), 3)
