
import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from time import sleep
from multiprocessing import shared_memory

class e_s2l():


    def __init__(self):
        # parameters
        self.amount = 1.0
        self.channel = 1.0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def return_values(self):
        # strings for GUI
        return [b's2l', b'amount', b'channel', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,1)), str(self.channel), '','') ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        self.amount = args[0]
        self.channel = int(args[1]*3)

        # print('-')
        # print(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
        # print(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')))
        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))

        # apply manipulation
        for i in range(3):
            #print(current_volume)
            world[i, :, :, :] *= (1-self.amount) + np.clip(current_volume,0,1)*self.amount

        return np.clip(world, 0, 1)
