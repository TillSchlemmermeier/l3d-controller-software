
import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from time import sleep
from generators.g_genhsphere import gen_hsphere
from multiprocessing import shared_memory


class g_soundsphere():
    def __init__(self):

        # parameters
        self.amount = 1.0
        self.channel = 10
        self.maxsize = 5
        self.smooth = 0.25
        self.speed = 1.0

        self.last_value = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def return_values(self):
        # strings for GUI
        return [b'SoundSphere', b'maxsize', b'channel', b'smooth', b'speed']


    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.maxsize,2)), str(round(self.channel,2)), str(round(self.smooth,2)),
        str(round(self.speed,2))), 'utf-8')


    def __call__(self, args):

        # process parameters
        self.maxsize = args[0]*10
        self.channel = int(args[1]*3)
        self.smooth = args[2] * 0.5
        self.speed = args[3]

        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))

        # mix with old value
        current_volume = (1-self.smooth) * current_volume + self.smooth * self.last_value

        if self.speed < 1.0:
            if current_volume < self.last_value:
                current_volume = self.last_value-self.speed**2


        current_volume = np.clip(current_volume,0,1)
        size = self.maxsize*current_volume

        self.last_value = current_volume
        world = np.zeros([3, 10, 10, 10])

        world[0, :, :, :] = gen_hsphere(size, 4.5, 4.5, 4.5)
        world[1:, :, :, :] = world[0, :, :, :]
        world[2:, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)
