# modules
import numpy as np


class e_blank():
    '''
    Effect: blank
    '''
    def __init__(self):
        pass

    #strings for GUI
    def return_values(self):
        return [b'blank', b'', b'', b'', b'']

    def __call__(self, world, args):
        return world
