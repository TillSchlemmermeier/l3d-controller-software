# modules
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
from multiprocessing import shared_memory

class e_rainbownew:
    '''
    Effect: Rainbow
    '''
    def __init__(self):
        self.speed = 0.5
        self.color = [0.1,0.0,0.0]
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4

    #strings for GUI
    def return_values(self):
        return [b'rainbow', b'speed', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), '', '', channel), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.speed = args[0]/10
        self.channel = int(args[3]*4)-1

        color = hsv_to_rgb(self.color[0], 1, 1)

        # check if s2l is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.color[0] += current_volume / 10

        else:
            self.color[0] += self.speed

        world[0, x, y, z] *= color[0]
        world[1, x, y, z] *= color[1]
        world[2, x, y, z] *= color[2]

        return np.clip(world, 0, 1)
