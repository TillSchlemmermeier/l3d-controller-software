
import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from time import sleep
from generators.g_cube import g_cube
from itertools import cycle
from multiprocessing import shared_memory

class g_soundcube():
    def __init__(self):
        # parameters
        self.amount = 1.0
        self.channel = 10
        self.threshold = 0.5

        self.sizes = cycle([0,1,2,3,4])
        self.size = 1
        self.cube = g_cube()

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def return_values(self):
        # strings for GUI
        return [b'soundcube', b'channel', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.channel,2)), '', '', ''),'utf-8')


    def __call__(self, args):

        # process parameters
        self.channel = int(args[0]*3)

        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))

        # apply threshold
        if current_volume > 0:
            self.size = next(self.sizes)

#        print(self.size)
        world = self.cube([self.size/4.0, 0, 0, 0])


        return np.clip(world, 0, 1)
