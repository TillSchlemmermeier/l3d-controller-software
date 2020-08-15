# modules
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere

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
        self.step = 0

    def return_values(self):
        return [b'growing_sphere', b'maxsize', b'speed', b'shape', b'']

    def return_gui_values(self):
        if self.oscillate < 0.3:
            osci = 'sin'
        elif self.oscillate > 0.7:
            osci = 'explode'
        else:
            osci = 'implode'
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.maxsize,2)), str(round(self.growspeed,2)), osci, ''),'utf-8')


    def __call__(self, args):
        self.maxsize = args[0]*10
        self.growspeed = args[1]
        self.oscillate = args[2]

        world = np.zeros([3, 10, 10, 10])

        # oscillates between 0 and 1
        if self.oscillate < 0.3:
            osci = np.sin(self.step*self.growspeed)*0.5 + 0.5
        elif self.oscillate > 0.7:
            osci = sawtooth(self.step*self.growspeed, 0)*0.5 + 0.5
        else:
            osci = sawtooth(self.step*self.growspeed)*0.5 + 0.5

        # scales to maxsize
        size = self.maxsize * osci
        self.step += 1
        # creates hollow sphere with parameters
        world[0, :, :, :] = gen_hsphere(size, 4.5, 4.5, 4.5)
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        return np.round(np.clip(world, 0, 1), 3)
