# modules
import numpy as np
from scipy.signal import fftconvolve
from scipy.signal.windows import gaussian

class e_mean_vertical():

    def __init__(self):
        self.amount = 0.1
        self.mean = np.zeros([5,5,5])
        self.mean[:, 2, 2] = 1/10.0

    def return_state(self):
        return [
            ['amount', 'amount', round(self.amount,1)],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount = args[0]
        # === PARAMETERS END ===

        for i in range(3):
            world[i, :, :, :] = (1-self.amount)*world[i, :, :, :] + self.amount*fftconvolve(world[i, :, :, :], self.mean, mode='same')

        return np.clip(world, 0, 1)
