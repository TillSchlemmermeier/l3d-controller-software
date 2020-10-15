
import numpy as np
#import pyaudio
#from scipy.fftpack import fft, fftfreq
import scipy
#import struct
from time import sleep
from colorsys import rgb_to_hsv, hsv_to_rgb
from multiprocessing import shared_memory

class e_sound_color():
    def __init__(self):

        # parameters
        # self.threshold = 0.5
        self.channel = 0
        self.colorstep = 0.1
        self.color = 0.0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def return_values(self):
        # strings for GUI
        return [b's2l', b'color stp', b'channel', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.colorstep,2)), str(self.channel), '', '') ,'utf-8')

    def __call__(self, world, args):

        # process parameters
        self.colorstep = 0.1*args[0]+0.001
        self.channel = int(args[1]*3)

        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))

        # check for threshold
        if current_volume > 0.0:
            self.color += self.colorstep

        color = hsv_to_rgb(self.color, 1, 1)
        world[0, :, :, :] *= color[0]
        world[1, :, :, :] *= color[1]
        world[2, :, :, :] *= color[2]

        return np.clip(world, 0, 1)
