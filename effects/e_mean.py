# modules
import numpy as np
from scipy.signal import fftconvolve, gaussian

class e_mean():

    def __init__(self):
        self.amount = 0.1
        self.mean = np.zeros([3,3,3])
        self.mean[:, :, :] = 1/18.0
        self.fade = 0.1

        self.fadeworld = np.zeros([3, 10, 10, 10])

    def return_values(self):
        return [b'mean', b'amount', b'fade', b'', b'']

    def __call__(self, world, args):
        # parsing input
        self.amount = args[0]
        self.fade = args[1]

        for i in range(3):
            world[i, :, :, :] = (1-self.fade)*world[i, :, :, :] + self.fade*self.fadeworld[i, :, :, :]
            world[i, :, :, :] = (1-self.amount)*world[i, :, :, :] + self.amount*fftconvolve(world[i, :, :, :], self.mean, mode='same')
            self.fadeworld[i, :, :, :] = np.clip(self.world[i, :, :, :], 0, 1)


        return np.clip(world, 0, 1)
