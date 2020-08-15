# modules
import numpy as np
from random import randint

class e_cut_cube():
    '''
    Effect: e_cut_cube
    '''

    def __init__(self):
        self.speed = 2
        self.step = 0

    #strings for GUI
    def return_values(self):
        return [b'cut_cube', b'speed', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed),2), '', '', ''), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.speed = (args[0]*10)+1

        num = randint(0,7)

        if self.step % self.speed == 0:

            if num == 0:
                world[:, :5, :5, :5] = 0
            if num == 1:
                world[:, :5, :5, 5:] = 0
            if num == 2:
                world[:, :5, 5:, :5] = 0
            if num == 3:
                world[:, 5:, :5, :5] = 0
            if num == 4:
                world[:, :5, 5:, 5:] = 0
            if num == 5:
                world[:, 5:, :5, 5:] = 0
            if num == 6:
                world[:, 5:, 5:, :5] = 0
            if num == 7:
                world[:, 5:, 5:, 5:] = 0

            self.step += 1

        return np.clip(world, 0, 1)
