# modules
import numpy as np
from scipy.signal import sawtooth
from generators.g_genhsphere import gen_hsphere
import pyaudio
import scipy
import struct
from random import randint
from scipy.fftpack import fft, fftfreq
from multiprocessing import shared_memory


class g_sound_sidesquares():

    def __init__(self):

        # get initial random lines
        self.lines = []
        for i in range(10):
            self.lines.append(self.gen_slice(randint(0,2), randint(0,1), randint(0,4)))

        self.counter = 1
        self.reset = 20
        self.number = 10
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def return_values(self):
        return [b'sound_sidesquares', b'reset', b'channel', b'number', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.reset), str(round(self.channel,2)), str(self.number), ''),'utf-8')

    def __call__(self, args):

        # process parameters
        self.reset = int(args[0]*20+1)
        self.channel = int(args[1]*3)
        self.number = int(args[2]*12 + 1)

        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
        # now we can world with the sound
        world = np.zeros([3, 10, 10, 10])

        # get lines
        for i in range(len(self.lines)):
            if current_volume > i*0.1:
                world[0, :, :, :] += self.lines[i]*(current_volume-i*0.1)
#                world[0, line[0], line[1], line[2]] = current_volume

        # copy to other colors
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        if self.counter > self.reset:
            self.lines = []
            # reset lines
            for i in range(self.number):
                self.lines.append(self.gen_slice(randint(0,2), randint(0,1), randint(0,4)))

            self.counter = 0

        self.counter += 1

        return np.round(np.clip(world, 0, 1), 3)

    def gen_slice(self, axis, dir, size, ):

        side = np.zeros([10, 10])
        world = np.zeros([10, 10, 10])

        side[0+size : 10-size, size] = 1
        side[0+size : 10-size, 9-size] = 1
        side[size, 0+size : 10-size] = 1
        side[9-size, 0+size : 10-size] = 1

        if axis == 0:
            if dir == 0 :
                world[0, :, :] = side[:, :]
            elif dir == 1:
                 world[9, :, :] = side[:, :]
        elif axis == 1:
            if dir == 0 :
                world[:, 0, :] = side[:, :]
            elif dir == 1:
                 world[:, 9, :] = side[:, :]
        elif axis == 2:
            if dir == 0 :
                world[:, :, 0] = side[:, :]
            elif dir == 1:
                 world[:, :, 9] = side[:, :]

        return world
