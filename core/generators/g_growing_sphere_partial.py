# modules
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere

# fortran routine is in g_growing_sphere_f.f90

class g_growing_sphere_partial():
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
        self.maxsize_variation = 1
        self.growspeed = 1
        self.growspeed_variation = 0
        self.step = 0

    def return_state(self):
        return [
            ['maxsize', 'maxsize', round(self.maxsize,2)],
            ['size var', 'maxsize_variation', round(self.maxsize_variation,2)],
            ['speed', 'growspeed', round(self.growspeed,2)],
            ['speed var', 'growspeed_variation', round(self.growspeed_variation,2)],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.maxsize = args[0]*10
        self.maxsize_variation = args[1]*2
        self.growspeed = args[2]
        self.growspeed_variation = args[3]*2
        # === PARAMETERS END ===

        world = np.zeros([3, 10, 10, 10])

        # first half
        osci = np.sin(self.step*self.growspeed)*0.5 + 0.5
        # scales to maxsize
        size = self.maxsize * osci

        # creates hollow sphere with parameters
        world[0, :, :, :] = gen_hsphere(size, 4.5, 4.5, 4.5)
        #world[1:, :, :, :] = world[0, :, :, :]
        #world[2:, :, :, :] = world[0, :, :, :]


        # second half
        osci = np.sin(self.step*(self.growspeed+self.growspeed_variation))*0.5 + 0.5
        # scales to maxsize
        size = (self.maxsize + self.maxsize_variation) * osci

        # creates hollow sphere with parameters
        world[0, :, 5:, :] = gen_hsphere(size, 4.5, 4.5, 4.5)[:, 5:, :]

        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        self.step += 1


        return np.round(np.clip(world, 0, 1), 3)
