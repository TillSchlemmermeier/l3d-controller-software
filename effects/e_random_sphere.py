# modules
import numpy as np
from effects.gen_outer_shadow_f import outer_shadow
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from multiprocessing import shared_memory


class e_outer_shadow():
    def __init__(self):
        self.amount = 1.0
        self.channel = 1

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

        self.size = 1
        self.amount = 0.0

    #Strings for GUI
    def return_values(self):
        return [b'outershadow', b'exponent', b'channel', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.exponent,2)),  str(round(self.channel,2)), '', ''),'utf-8')

    def __call__(self, world, args):
        self.exponent = args[0]*4
        self.channel = int(args[1]*4)
        # self.amount = args[2]

        current_volume = np.clip(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')),0,5)

        bla = outer_shadow(self.exponent*current_volume, 5.5, 5.5, 5.5)
        world[0, :, :, :] -= bla
        world[1, :, :, :] -= bla
        world[2, :, :, :] -= bla

        return np.clip(world, 0, 1)