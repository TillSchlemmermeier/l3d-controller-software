# modules
from itertools import cycle
from multiprocessing import shared_memory
import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from multiprocessing import shared_memory

class g_conway():

    def __init__(self):
        # parameters
        self.speed = 1
        self.wait = 20
        self.lastvalue = 0
        self.step = 0
        self.mode = 0

        self.sides = np.random.randint(0, 2, [40,10])
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")


    def return_values(self):
        return [b'conway', b'speed', b'wait', b'mode', b'']

    def return_gui_values(self):
        if self.mode == 1:
            return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.speed), str(self.wait), str(self.mode), 'trigger'),'utf-8')

        else:
            return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.speed), str(self.wait), str(self.mode), ''),'utf-8')


    def life_step_1(self, X):
        """Game of life step using generator expressions"""
        nbrs_count = sum(np.roll(np.roll(X, i, 0), j, 1)
                        for i in (-1, 0, 1) for j in (-1, 0, 1)
                        if(i != 0 or j != 0))
        return (nbrs_count == 3) | (X & (nbrs_count == 2))


    def __call__(self, args):
        self.speed = int(args[0]*6)+1
        self.wait = int(args[1]*50)+10
        if args[2] < 0.5:
            self.mode = 0
        else:
            self.mode = 1

        # check for Trigger
        if self.mode == 1:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:

                self.lastvalue = current_volume
                self.sides += np.random.randint(0, 2, [40,10])
                # self.sides = np.clip(self.sides, 0, 2)
        else:
            pass
        self.step += 1


        # transfer to real world
        world = np.zeros([3, 10, 10, 10])
        for i in range(3):
            world[i, :, :, 0] = self.sides[:10, :]
            world[i, :, 0, :] = self.sides[10:20, :]
            world[i, :, :, 9] = self.sides[20:30, :]
            world[i, :, 9, :] = self.sides[30:, :]

        if self.step % self.speed == 0:
            self.sides = self.life_step_1(self.sides)

        if self.mode == 0:
            if self.step % self.wait == 0:
                self.sides += np.random.randint(0, 2, [40,10])
                # self.sides -= np.random.randint(0, 2, [40,10])
                # self.sides = np.clip(self.sides, 0, 2)

        return np.clip(np.round(world,2), 0, 1)
