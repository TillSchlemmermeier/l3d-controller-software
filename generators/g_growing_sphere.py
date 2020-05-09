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


    #Strings for GUI
    def return_values(self):
        return [b'growing_sphere', b'maxsize', b'growspeed', b'oscillate (sin/sawtooth)', b'']

    #def control(self, maxsize, growspeed, oscillate):
    def __call__(self, args):
        self.maxsize = args[0]*10
        self.growspeed = args[1]
        self.oscillate = args[2]

#def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # oscillates between 0 and 1
        if self.oscillate < 0.3:
            osci = np.sin(self.step*self.growspeed)*0.5 + 1
        elif self.oscillate > 0.7:
            osci = sawtooth(self.step*self.growspeed, 0)*0.5 + 1
        else:
            osci = sawtooth(self.step*self.growspeed)*0.5 + 1

        # scales to maxsize
        size = self.maxsize * osci
        self.step += 1
        # creates hollow sphere with parameters
        world[0, :, :, :] = gen_hsphere(size, 4.5, 4.5, 4.5)
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        return np.round(np.clip(world, 0, 1), 3)
