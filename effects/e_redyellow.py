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

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,1)), '', '', ''), 'utf-8')


    def __call__(self, world, args):
        # parse input
        self.speed = args[0]*0.1


        self.green = np.sin(self.speed*self.step)

        world[0, :, :, :] = world[0, :, :, :]*self.red
        world[1, :, :, :] = world[1, :, :, :]*self.green
        world[2, :, :, :] = world[2, :, :, :]*self.blue

        self.step += 1

        return np.clip(world, 0, 1)
