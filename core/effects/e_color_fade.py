# modules
import numpy as np
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory

class e_color_fade():
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
        self.lastvalue = 0
        self.channel = 0
        self.color = [0,0,0]

    def return_state(self):
        return [
            ['speed', 'speed', round(self.speed,2)],
            ['Color 1', 'color1', round(self.color1,1)],
            ['Color 2', 'color2', round(self.color2,1)],
            ['channel', 'channel', self.channel],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.speed = args[0]
        self.color1 = args[1]
        self.color2 = args[2]
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][round(args[3]*5)]
        # === PARAMETERS END ===

        # check if s2l is activated
        if isinstance(self.channel, int):
            current_volume = np.clip(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')), 0, 1)

            self.step = (current_volume * np.pi) / self.speed

        # check if trigger is activated
        elif self.channel == 'Trigger':
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            #check if trigger has been activated
            if current_volume > self.lastvalue:
                self.step = 0
                self.lastvalue = current_volume

            #limit cos to 2*pi until new trigger
            if (self.step * self.speed) > (2 * np.pi):
                self.step = (2 * np.pi) / self.speed

        # calculate color
        if self.color1 < self.color2:
            self.balance = self.color1 + (self.color2 - self.color1) * ((np.cos(self.speed*self.step)*0.5)+0.5)
        else:
            self.balance = self.color1 + (1 - self.color1 + self.color2) * ((np.cos(self.speed*self.step)*0.5)+0.5)

        try:
            self.color = hsv_to_rgb(float(np.clip(self.balance, 0, 1)), 1, 1)
        except:
            pass

        for i in range(3):
            world[i, :, :, :] *= self.color[i]

        self.step += 1

        return np.clip(world, 0, 1)
