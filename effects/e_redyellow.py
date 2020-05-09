# modules
import numpy as np


class e_redyellow():
    '''
    Effect: redyellow

    '''

    def __init__(self):
        self.speed = 0.5
        self.red = 1.0
        self.green = 1.0
        self.blue = 0.0
        self.step = 0

    #strings for GUI
    def return_values(self):
        return [b'redyellow', b'speed', b'', b'', b'']

    def __call__(self, world, args):
        # parse input
        self.speed = args[0]*0.1


        self.green = np.sin(self.speed*self.step)

        world[0, :, :, :] = world[0, :, :, :]*self.red
        world[1, :, :, :] = world[1, :, :, :]*self.green
        world[2, :, :, :] = world[2, :, :, :]*self.blue

        self.step += 1

        return world
