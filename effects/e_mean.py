# modules
import numpy as np
from scipy.signal import fftconvolve, gaussian

class e_mean():

    def __init__(self):
        self.amount = 0.1
        self.mean = np.zeros([3,3,3])
        self.mean[:, :, :] = 1/18.0

    #strings for GUI
    def return_values(self):
        return [b'mean', b'amount', b'', b'', b'']


    def __call__(self, world, args):
        # parsing input
        self.amount = args[0]

        for i in range(3):
            world[i, :, :, :] = (1-self.amount)*world[i, :, :, :] + self.amount*fftconvolve(world[i, :, :, :], self.mean, mode='same')

        return np.clip(world, 0, 1)
