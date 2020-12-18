# modules
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
from multiprocessing import shared_memory


class e_sound_gradient():
    '''
    '''

    def __init__(self):

        self.c1 = 0.1 # [0.1,0.0,0.0]
        self.c2 = 0.4 # [0.4,0.4,0.0]
        self.balance = 1.0

        self.channel = 0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    #strings for GUI
    def return_values(self):
        return [b's2lgrad', b'Color 1', b'Color 2',  b'channel', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.c1,1)), str(round(self.c2,1)), str(self.channel), ''), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.c1 = args[0] # hsv_to_rgb(c1,1,1)
        self.c2 = args[1] # hsv_to_rgb(c2,1,1)
        # self.balance = 1 - (2 * args[2])
        self.channel = int(args[2]*3)

        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
        current_color = self.sigmoid(current_volume*10-4.5)*(self.c1-self.c2)+self.c2

        # choose color according to x position
        for x in range(10):
            color = hsv_to_rgb(current_color,1,1)
            world[0,x,:,:] = world[0,x,:,:] * color[0]
            world[1,x,:,:] = world[1,x,:,:] * color[1]
            world[2,x,:,:] = world[2,x,:,:] * color[2]

        return np.clip(world, 0, 1)


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x*self.balance))
