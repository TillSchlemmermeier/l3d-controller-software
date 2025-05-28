# modules
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
from multiprocessing import shared_memory

class e_gradient():
    '''
    '''

    def __init__(self):

        self.c1 = 0.1
        self.c2 = 0.4
        self.old_c1 = 0.1
        self.old_c2 = 0.4
        self.channel = 0

        self.balance = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def return_state(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return [
            ['Color 1', 'c1', round(self.c1,1)],
            ['Color 2', 'c2', round(self.c2,1)],
            ['balance', 'balance', round(self.balance,1)],
            ['channel', 'channel', channel],
        ]

    def __call__(self, world, args):
        # parsing input
        self.c1 = args[0] # hsv_to_rgb(c1,1,1)
        self.c2 = args[1] # hsv_to_rgb(c2,1,1)
        self.balance = 1 - (2 * args[2])
        self.channel = int(args[3]*4)-1


        # generate color list
        x = np.array([0,1,2,3,4,5,6,7,8,9])

        if self.channel >= 0:
            # sound modus
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))

            # apply threshold
            if current_volume > 0:
                self.old_c1 += current_volume/50
                self.old_c2 += current_volume/50

            y = self.sigmoid(x-4.5)*(self.old_c1-self.old_c2)+self.old_c2

        else:
            y = self.sigmoid(x-4.5)*(self.c1-self.c2)+self.c2
            self.old_c1 = self.c1
            self.old_c2 = self.c2

        # choose color according to x position
        for x in range(10):
            color = hsv_to_rgb(y[x],1,1)
            for i in range(3):
                world[i,x,:,:] = world[i,x,:,:] * color[i]

        return np.clip(world, 0, 1)


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x[:]*self.balance))
