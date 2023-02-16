# modules
import numpy as np
from effects.gen_outer_shadow_f import outer_shadow
#import pyaudio
#from scipy.fftpack import fft, fftfreq
#import scipy
#import struct
from multiprocessing import shared_memory


class e_outer_shadow():
    def __init__(self):
        self.amount = 1.0
        self.channel = 1
        self.exponent = 1
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

        self.size = 1
        self.amount = 0.0

    #Strings for GUI
    def return_values(self):
        return [b'outershadow', b'exponent', b'amount', b'', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel < 0:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.exponent,2)),  str(round(self.amount,2)), '', channel),'utf-8')

    def __call__(self, world, args):
        self.exponent = args[0]*3+1
        self.channel = int(args[3]*5)-1
        self.amount = args[1]
        # self.amount = args[2]
        if self.channel >= 0:
            current_volume = np.clip(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')),0,5)
        else:
            current_volume = 1

        bla = outer_shadow(self.exponent*current_volume, 5.5, 5.5, 5.5)*self.amount
        world[0, :, :, :] -= bla
        world[1, :, :, :] -= bla
        world[2, :, :, :] -= bla

        return np.clip(world, 0, 1)
