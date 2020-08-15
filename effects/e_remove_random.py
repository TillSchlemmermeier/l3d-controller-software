# modules
import numpy as np
from random import randint

class e_remove_random():

    def __init__(self):
        self.n = 1

    #strings for GUI
    def return_values(self):
        return [b'remove_random', b'speed', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.n), '', '', ''), 'utf-8')


    def __call__(self, world, args):
        # parsing input
        self.n = int(args[0]*200)+1

        for i in range(self.n):
            world[:, randint(0,9), randint(0,9), randint(0,9)] = 0.0

        return np.clip(world, 0, 1)
