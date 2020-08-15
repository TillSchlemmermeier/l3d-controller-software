# modules
import numpy as np


class e_fade2blue():
    '''
    Effect: fade2blue

    fades the cube to blue by moving some of the green and red
    to the blue

    Parameters:
    - amount: how much is moved from the r/g channel to the b channel
    '''

    def __init__(self):
        self.amount = 0.5

    #strings for GUI
    def return_values(self):
        return [b'fade2blue', b'amount', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,2)), '', '', ''), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.amount = args[0]

        world[2, :, :, :] += self.amount*world[0, :, :, :] + self.amount*world[1, :, :, :]
        world[:2, :, :, :] -= world[:2, :, :, :]*self.amount

        return np.clip(world, 0, 1)
