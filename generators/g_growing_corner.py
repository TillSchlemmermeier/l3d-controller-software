# modules
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere

# fortran routine is in g_growing_sphere_f.f90

class g_growing_corner():
    '''
    Generator: growing_corner

    a growing hollow sphere from a corner of the cube

    Parameters:
    - maxsize
    - growspeed
    - oscillate y/n
    '''

    def __init__(self):
        self.maxsize = 10
        self.growspeed = 1
        self.steps = 0

    def label(self):
        return ['maxsize',round(self.maxsize,2),'growspeed',round(self.growspeed,2),'Steps',round(self.steps,2)]

    def control(self, maxsize, growspeed, steps):
        self.maxsize = maxsize*10
        self.growspeed = growspeed
        self.steps = steps

    xpos = 9*randint(0,1)
    ypos = 9*randint(0,1)
    zpos = 9*randint(0,1)

    for x in range (0,steps)
        def generate(self, step, dumpworld):
            world = np.zeros([3, 10, 10, 10])

            # oscillates between 0 and 1
            osci = np.sin(step*self.growspeed)*0.5 + 1

            # scales to maxsize
            size = self.maxsize * osci
            # creates hollow sphere with parameters
            world[0, :, :, :] = gen_hsphere(size,xpos,ypos,zpos)
            world[1:, :, :, :] = world[0, :, :, :]
            world[2:, :, :, :] = world[0, :, :, :]

            return np.round(np.clip(world, 0, 1), 3)
