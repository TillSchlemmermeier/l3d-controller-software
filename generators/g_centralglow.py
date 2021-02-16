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
        self.channel = 1
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.size = 1
        self.exponent = 1
        self.lastvalue = 0
        self.counter = 0

    #Strings for GUI
    def return_values(self):
        return [b'centralglow', b'exponent', b'channel', b'', b'']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = "Trigger"

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.exponent,2)),  str(round(self.channel,2)), '', ''),'utf-8')

    def __call__(self, args):
        self.exponent = args[0]*8
        self.channel = int(args[1]*4)

        world = np.zeros([3, 10, 10, 10])

        if 4 > self.channel >= 0:
            current_volume = np.clip(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')),0,3)

        #check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0

            if self.counter < 11:
                current_volume = 1 - (self.counter / 10)
                self.counter += 1

        bla = gen_central_glow(6-self.exponent*current_volume, 5.5, 5.5, 5.5)
        world[0, :, :, :] = bla
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)
