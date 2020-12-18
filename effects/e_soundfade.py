
import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from time import sleep
from multiprocessing import shared_memory

class e_soundfade():


    def __init__(self):
        # parameters
        self.amount = 1.0
        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastworld = np.zeros([3,10,10,10])

    def return_values(self):
        # strings for GUI
        return [b'soundfade', b'amount', b'channel', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,1)), str(self.channel), '','') ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        self.amount = args[0]*2
        self.channel = int(args[1]*3)

        current_volume = self.amount*float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))**4

        current_volume = np.clip(current_volume, 0, 1)

        for i in range(3):
            world[i, :, :, :] = (1-current_volume) * world[i, :, :, :] + current_volume*self.lastworld[i, :, :, :]
            self.lastworld[i, :, :, :] = world[i, :, :, :]


        return np.clip(world, 0, 1)
