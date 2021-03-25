# modules
import numpy as np
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory
from random import random

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
        self.Trigger = 0
        self.lastvalue = 0

    #strings for GUI
    def return_values(self):
        return [b'rainbow', b'speed', b'', b'', b'S2L Trigger']

    def return_gui_values(self):
        if 0.2 > self.Trigger >= 0:
            channel = "Off"
        elif 0.8 > self.Trigger >= 0.2:
            channel = "On"
        else:
            channel = "random"

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(20*self.speed,2)), '', '', channel), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.speed = (args[0]**2)/20
        self.Trigger = args[3]

        color = hsv_to_rgb(self.color[0], 1, 1)

        # check if s2l is activated
        if self.Trigger >= 0.2:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                if self.Trigger < 0.8:
                    self.color[0] += self.speed * 2
                else:
                    self.color[0] = random()

        else:
            self.color[0] += self.speed

        for i in range(3):
            world[i, :, :, :] *= color[i]

        return np.clip(world, 0, 1)
