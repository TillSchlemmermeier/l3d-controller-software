# modules
import numpy as np
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory
from random import random

class e_rainbow():
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

    def return_state(self):
        if 0.2 > self.Trigger >= 0:
            channel = "Off"
        elif 0.8 > self.Trigger >= 0.2:
            channel = "On"
        else:
            channel = "random"
            
        # return [Display Name, Viariable Name, Display Value] for each parameter
        return [
            ['speed', 'speed', round(20*self.speed,2)],
            ['S2L Trigger', 'Trigger', channel],
        ]

    def __call__(self, world, args):
        # parsing input
        self.speed = (args[0]**2)/50
        self.Trigger = args[1]

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
