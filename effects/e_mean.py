# modules
import numpy as np
from scipy.signal import fftconvolve, gaussian

class e_mean():

    def __init__(self):
        self.amount = 0.1
        self.mean = np.zeros([3,3,3])
        self.mean[:, :, :] = 1/18.0


    def control(self, amount, blub0, blub1):
        self.amount = amount

    def label(self):
        return ['blur amount', np.round(self.amount, 2),'empty', 'empty','empty','empty']

    def generate(self, step, world):

        for i in range(3):
            world[i, :, :, :] = (1-self.amount)*world[i, :, :, :] + self.amount*fftconvolve(world[i, :, :, :], self.mean, mode='same')

        return np.clip(world, 0, 1)
