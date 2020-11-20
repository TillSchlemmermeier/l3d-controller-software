# modules
import numpy as np
from scipy.signal import fftconvolve, gaussian
from multiprocessing import shared_memory

class e_sound_mean():

    def __init__(self):
        self.amount = 0.1
        self.fade = 0.1
        self.fadeworld = np.zeros([3, 10, 10, 10])
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 1

    def return_values(self):
        return [b'sound mean', b'amount', b'fade', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,1)), str(round(self.fade,1)), '', ''), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.amount = args[0]
        self.fade = args[1]

        width = self.amount * float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))

        gaussian = self.gaussian_2d(width)

        for i in range(3):
            for j in range(10):
                world[i, j, :, :] = (1-self.fade)*np.clip(world[i, j, :, :]) + self.fade*self.fadeworld[i, j, :, :]
                world[i, j, :, :] = (1-self.amount)*world[i, j, :, :] + self.amount*fftconvolve(world[i, j, :, :], gaussian, mode='same')

                self.fadeworld[i, j, :, :] = np.clip(world[i, j, :, :], 0, 1)


        return np.clip(world, 0, 1)

    def gaussian_2d(self, width):
        x, y = np.meshgrid(np.linspace(-1,1,10), np.linspace(-1,1,10))
        d = np.sqrt(x*x+y*y)
        sigma = width
        g = np.exp(-( d**2 / ( 2.0 * sigma**2 ) ) )
        return g
