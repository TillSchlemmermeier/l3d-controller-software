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
        self.lastvalue = 0
        self.channel = 0

    #strings for GUI
    def return_values(self):
        return [b'colorfade', b'speed', b'Color 1', b'Color 2', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel < 0:
            channel = 'noS2L'
        else:
            channel = 'Trigger'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), str(round(self.color1,1)), str(round(self.color2,1)), channel), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.speed = args[0]
        self.color1 = args[1]
        self.color2 = args[2]
        self.channel = int(args[3]*5)-1

        #check if s2l is activated
        if 4 > self.channel >= 0:
            current_volume = np.clip(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')), 0, 1)
            self.step = (current_volume * np.pi) / self.speed

        #check if trigger is activated
        elif self.channel > 3 :
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            #check if trigger has been activated
            if current_volume > self.lastvalue:
                self.step = 0
                self.lastvalue = current_volume

            #limit cos to 2*pi until new trigger
            if (self.step * self.speed) > (2 * np.pi):
                self.step = (2 * np.pi) / self.speed

        #calculate color
        if self.color1 < self.color2:
            self.balance = self.color1 + (self.color2 - self.color1) * ((np.cos(self.speed*self.step)*0.5)+0.5)
        else:
            self.balance = self.color1 + (1 - self.color1 + self.color2) * ((np.cos(self.speed*self.step)*0.5)+0.5)

        color = hsv_to_rgb(self.balance, 1, 1)

        for i in range(3):
            world[i, :, :, :] *= color[i]

        self.step += 1

        return np.clip(world, 0, 1)
