# modules
import numpy as np
from random import uniform

class e_random_brightness():

    def __init__(self):
        self.speed = 1
        self.brightness = uniform(0,1)
        self.step = 0

    #strings for GUI
    def return_values(self):
        return [b'random_brightness', b'speed', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,1)), '', '', ''), 'utf-8')


    def __call__(self, world, args):
        # parsing input
        self.speed = int(args[0]*10)+1

        if self.step % self.speed == 0:
            self.brightness = uniform(0, 1)

        self.step += 1

        return np.clip(world*self.brightness, 0, 1)
