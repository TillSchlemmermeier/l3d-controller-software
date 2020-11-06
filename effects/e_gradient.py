# modules
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
from multiprocessing import shared_memory


class e_gradient():
    '''
    '''

    def __init__(self):

        self.c1 = 0.1 # [0.1,0.0,0.0]
        self.c2 = 0.4 # [0.4,0.4,0.0]
        self.old_c1 = 0.1
        self.old_c2 = 0.4

        self.balance = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
#        self.oldy = [0,1,2,3,4,5,6,7,8,9]

    #strings for GUI
    def return_values(self):
        return [b'gradient', b'Color 1', b'Color 2', b'balance', b'channel']

    def return_gui_values(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.c1,1)), str(round(self.c2,1)), str(round(self.balance,1)), channel), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.c1 = args[0] # hsv_to_rgb(c1,1,1)
        self.c2 = args[1] # hsv_to_rgb(c2,1,1)
        self.balance = 1 - (2 * args[2])
        self.channel = int(args[3]*4)-1

        '''
        if self.c2 > self.c1:
            temp = self.c1
            self.c1 = self.c2
            self.c2 = temp
        '''

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
            world[0,x,:,:] = world[0,x,:,:] * color[0]
            world[1,x,:,:] = world[1,x,:,:] * color[1]
            world[2,x,:,:] = world[2,x,:,:] * color[2]

        return np.clip(world, 0, 1)


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x[:]*self.balance))
