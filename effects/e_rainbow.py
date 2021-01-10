# modules
import numpy as np
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory

class e_rainbow:
    '''
    Effect: Rainbow colors

    Parameters:
    speed of color shift
    Sound2Light channel, volume drives color shift
    '''
    def __init__(self):
        self.speed = 0.5
        self.color = [0.1,0.0,0.0]
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4
        self.lastvalue = 0

    #strings for GUI
    def return_values(self):
        return [b'rainbow', b'speed', b'', b'', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
                channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(20*self.speed,2)), '', '', channel), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.speed = args[0]/20
        self.channel = int(args[3]*5)-1

        color = hsv_to_rgb(self.color[0], 1, 1)

        # check if s2l is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.color[0] += current_volume / 10
        elif self.channel > 3 :
            current_volume = int(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.color[0] += 0.05

        else:
            self.color[0] += self.speed


        # check if s2l is activated


        world[0, :, :, :] *= color[0]
        world[1, :, :, :] *= color[1]
        world[2, :, :, :] *= color[2]

        return np.clip(world, 0, 1)
