# modules
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

    def return_values(self):
        return [b'growing_sphere', b'maxsize', b'speed', b'shape', b'S2L Trigger']

    def return_gui_values(self):
        if self.oscillate < 0.3:
            osci = 'sin'
        elif self.oscillate > 0.7:
            osci = 'implode'
        else:
            osci = 'explode'

        if self.trigger:
            trigger = 'On'
        else:
            trigger = 'Off'
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.maxsize,2)), str(round(self.growspeed,2)), osci, trigger),'utf-8')


    def __call__(self, args):
        self.maxsize = args[0]*15
        self.growspeed = args[1]*2
        self.oscillate = args[2]
        if args[3] > 0.2:
            self.trigger = True
        else:
            self.trigger = False

        world = np.zeros([3, 10, 10, 10])

        if self.trigger:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.pos = [randint(0,9), randint(0,9), randint(0,9)]
                self.stop = False

            if (self.step*self.growspeed) % (2*np.pi) < self.growspeed:
                self.stop = True

            if self.stop:
                self.step = 0

        # oscillates between 0 and 1
        if self.oscillate < 0.3:
            osci = 1 - (np.cos(self.step*self.growspeed)*0.5 + 0.5)
        elif self.oscillate > 0.7:
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
