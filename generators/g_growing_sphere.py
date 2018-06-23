# modules
import numpy as np
from scipy.signal import sawtooth
from g_growing_sphere_f import gen_hsphere

# fortran routine is in g_growing_sphere_f.f90

class g_growing_sphere():
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
        self.oscillate = 0

    def label(self):
        return ['maxsize',round(self.maxsize,2),'growspeed',round(self.growspeed,2),'oscillate?',round(self.oscillate,2)]

    def control(self, maxsize, growspeed, oscillate):
        self.maxsize = maxsize*10
        self.growspeed = growspeed
        self.oscillate = oscillate

    def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # oscillates between 0 and 1
        if self.oscillate < 0.5:
            osci = np.sin(step*self.growspeed)*0.5 + 1
        else:
            osci = sawtooth(step*self.growspeed)*0.5 + 1

        # scales to maxsize
        size = self.maxsize * osci
        # creates hollow sphere with parameters
        world[0, :, :, :] = gen_hsphere(size, 4.5,4.5,4.5)
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        return np.round(np.clip(world, 0, 1), 3)
