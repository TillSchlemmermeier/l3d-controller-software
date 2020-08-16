# modules
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere
from random import randint
# fortran routine is in g_growing_sphere_f.f90

class g_growing_sphere_rand():
    '''
    Generator: growing_sphere

    a growing hollow sphere in the middle of the cube

    Parameters:
    - maxsize
    - growspeed
    - oscillate y/n
    '''

    def __init__(self):
        self.maxsize = 15
        self.growspeed = 1
        self.oscillate = 0
        self.step = 1
        self.pos = [randint(0,9), randint(0,9), randint(0,9)]
        self.wait = 15

    def return_values(self):
        return [b'growing_sphere', b'maxsize', b'speed', b'shape', b'refr_fram']

    def return_gui_values(self):
        if self.oscillate < 0.3:
            osci = 'sin'
        elif self.oscillate > 0.7:
            osci = 'implode'
        else:
            osci = 'explode'
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.maxsize,2)), str(round(self.growspeed,2)), osci, str(self.wait)),'utf-8')


    def __call__(self, args):
        self.maxsize = args[0]*15
        self.growspeed = args[1]
        self.oscillate = args[2]
        self.wait = int(1 / (self.growspeed * 2 * np.pi + 0.01)) + 1

        if self.step % self.wait == 0:
            self.pos = [randint(0,9), randint(0,9), randint(0,9)]

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
        world[0, :, :, :] = gen_hsphere(size, self.pos[0]-0.5, self.pos[1]-0.5, self.pos[2]-0.5)
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        return np.round(np.clip(world, 0, 1), 3)
