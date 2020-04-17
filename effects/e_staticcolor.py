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

    def return_values(self):
        return [['', ''],
				['', ''],
				['', '']]

    def __call__(self, world, args):

        self.red   = args[0]
        self.green = args[1]
        self.blue  = args[2]

        world[0, :, :, :] = world[0, :, :, :]*self.red
        world[1, :, :, :] = world[1, :, :, :]*self.green
        world[2, :, :, :] = world[2, :, :, :]*self.blue

        return np.clip(world, 0, 1)
