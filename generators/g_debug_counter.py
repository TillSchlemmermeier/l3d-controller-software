# modules
from itertools import cycle
from multiprocessing import shared_memory
import numpy as np

class g_debug_counter():
    '''
    Generator: cube
    a cube in the cube
    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    - s2l channel
    '''

    def __init__(self):
        # parameters
        self.step = 0

    #Strings for GUI
    def return_values(self):
        return [b'debug counter', b'', b'', b'', b'']

    def return_gui_values(self):

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format('', '', '', ''),'utf-8')


    def __call__(self, args):
        world = np.zeros([3,10,10,10])

        world[:, 0, 0, 0] = self.step%2

        if self.step % 4 == 0:
            world[:, 1, 0,0] = 1

        if self.step % 8 == 0:
            world[:, 2, 0,0] = 1

        if self.step % 16 == 0:
            world[:, 3, 0,0] = 1

        self.step += 1
        return np.clip(world, 0, 1)
