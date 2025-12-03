# modules
import struct
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere
from random import randint
from multiprocessing import shared_memory
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
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.trigger = False
        self.lastvalue = 0
        self.stop = False

    def return_state(self):
        return [
            ['maxsize', 'maxsize', round(self.maxsize,2)],
            ['speed', 'growspeed', round(self.growspeed,2)],
            ['shape', 'oscillate', self.oscillate],
            ['S2L Trigger', 'trigger', 'On' if self.trigger else 'Off'],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.maxsize = args[0]*15
        self.growspeed = args[1]*2
        self.oscillate = ['sin', 'explode', 'implode'][round(args[2]*2)]
        self.trigger = args[3] > 0.2
        # === PARAMETERS END ===

        world = np.zeros([3, 10, 10, 10])

        if self.trigger:
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.pos = [randint(0,9), randint(0,9), randint(0,9)]
                self.stop = False

            if (self.step*self.growspeed) % (2*np.pi) < self.growspeed:
                self.stop = True

            if self.stop:
                self.step = 0

        # oscillates between 0 and 1
        if self.oscillate == 'sin':
            osci = 1 - (np.cos(self.step*self.growspeed)*0.5 + 0.5)
        elif self.oscillate == 'implode':
            osci = sawtooth(self.step*self.growspeed, 0)*0.5 + 0.5
        else:
            osci = sawtooth(self.step*self.growspeed)*0.5 + 0.5

        if not self.trigger:
            # check for maximum
            if (self.step*self.growspeed) % (2*np.pi) < self.growspeed:
                self.pos = [randint(0,9), randint(0,9), randint(0,9)]

        # scales to maxsize
        size = self.maxsize * osci
        self.step += 1
        
        # creates hollow sphere with parameters
        world[0, :, :, :] = gen_hsphere(size, self.pos[0]-0.5, self.pos[1]-0.5, self.pos[2]-0.5)
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        return np.round(np.clip(world, 0, 1), 3)
