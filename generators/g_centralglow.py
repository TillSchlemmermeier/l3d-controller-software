# modules
import numpy as np
from generators.gen_central_glow_f import gen_central_glow
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from multiprocessing import shared_memory


class g_centralglow():
    def __init__(self):
        self.amount = 1.0
        # sound2light stuff
        self.sample_rate = 44100
        self.buffer_size = 2**11
        self.thres_factor = 0
        self.channel = 1

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

        self.threshold = 0.5

        self.size = 1

    #Strings for GUI
    def return_values(self):
        return [b'centralglow', b'exponent', b'channel', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.exponent,2)),  str(round(self.channel,2)), '', ''),'utf-8')

    def __call__(self, args):
        self.exponent = args[0]*8
        self.channel = int(args[1]*4)

        world = np.zeros([3, 10, 10, 10])

        current_volume = np.clip(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')),0,5)

        bla = gen_central_glow(6-self.exponent*current_volume, 5.5, 5.5, 5.5)
        world[0, :, :, :] = bla
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)
