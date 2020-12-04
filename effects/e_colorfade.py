# modules
import numpy as np
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory

class e_colorfade():
    '''
    Effect: colorfade
    Color fades between two colorsys

    Parameters:
    speed of colorshift
    color 1
    color 2
    '''

    def __init__(self):
        self.speed   = 0.5
        self.color1  = 0.1
        self.color2  = 0.2
        self.balance = 0.1
        self.step = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4

    #strings for GUI
    def return_values(self):
        return [b'newgradient', b'speed', b'Color 1', b'Color 2', b'channel']

    def return_gui_values(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,1)), str(round(self.color1,1)), str(round(self.color2,1)), channel), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.speed = args[0]/5
        self.color1 = args[1]
        self.color2 = args[2]
        self.channel = int(args[3]*4)-1

        # check if s2l is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.color1 += current_volume / 20
            self.color2 += current_volume / 20

        if self.color1 < self.color2:
            self.balance = self.color1 + (self.color2 - self.color1) * ((np.sin(self.speed*self.step)*0.5)+0.5)
        else:
            self.balance = self.color2 + (self.color1 - self.color2) * ((np.sin(self.speed*self.step)*0.5)+0.5)

        color = hsv_to_rgb(self.balance, 1, 1)

        world[0, :, :, :] *= color[0]
        world[1, :, :, :] *= color[1]
        world[2, :, :, :] *= color[2]

        self.step += 1

        return np.clip(world, 0, 1)
