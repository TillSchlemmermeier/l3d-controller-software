# modules
import numpy as np
from scipy.signal import fftconvolve
from scipy.signal.windows import gaussian

class e_mean_up_down():

    def __init__(self):
        self.amount = 0.1
        self.mean_up = np.zeros([5,5,5])
        self.mean_down = np.zeros([5,5,5])

        self.mean_up[2,2,2] = 1.0
        self.mean_up[1,2,2] = 0.25
        self.mean_up[0,2,2] = 0.05

        self.mean_down[2,2,2] = 1.0
        self.mean_down[3,2,2] = 0.25
        self.mean_down[4,2,2] = 0.05


        self.fade = 0.1
        self.dir = 'down'

        self.fadeworld = np.zeros([3, 10, 10, 10])

    def return_state(self):
        return [
            ['amount', 'amount', round(self.amount,1)],
            ['fade', 'fade', round(self.fade,1)],
            ['direction', 'dir', self.dir],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount = args[0]
        self.fade = args[1]
        self.dir = ['up', 'down'][round(args[2])]
        # === PARAMETERS END ===

        if self.dir == 'up':
            fade = self.mean_up
        else:
            fade = self.mean_down

        for i in range(3):
            world[i, :, :, :] = (1-self.fade)*world[i, :, :, :] + self.fade*self.fadeworld[i, :, :, :]
            world[i, :, :, :] = (1-self.amount)*world[i, :, :, :] + self.amount*fftconvolve(world[i, :, :, :], fade, mode='same')
            self.fadeworld[i, :, :, :] = np.clip(world[i, :, :, :], 0, 1)

        return np.clip(world, 0, 1)
