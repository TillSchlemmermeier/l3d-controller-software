# modules
import numpy as np

class e_staticcolor():
    '''
    Effect: static color
    Parameters:
    - red
    - green
    - blue
    '''
    def __init__(self):
        self.red = 1.0
        self.green = 1.0
        self.blue = 1.0

    #strings for GUI
    def return_values(self):
        return [b'staticcolor', b'Red', b'Green', b'Blue', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.red,1)), str(round(self.green,1)), str(round(self.blue,1)), ''), 'utf-8')

    def __call__(self, world, args):

        self.red   = args[0]
        self.green = args[1]
        self.blue  = args[2]

        world[0, :, :, :] = world[0, :, :, :]*self.red
        world[1, :, :, :] = world[1, :, :, :]*self.green
        world[2, :, :, :] = world[2, :, :, :]*self.blue

        return np.clip(world, 0, 1)
