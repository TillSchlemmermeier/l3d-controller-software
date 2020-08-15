# modules
import numpy as np

class e_squared():

    def __init__(self):
        self.exponent = 1

    #strings for GUI
    def return_values(self):
        return [b'squared', b'exponent', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.exponent,1)), '', '', '', 'utf-8')



    def __call__(self, world, args):
        # parsing input
        self.exponent = 0.5 + args[0]*2

        world = world**self.exponent

        return np.clip(world, 0, 1)
