# modules
import numpy as np


class g_blank():
    '''
    Generator: blank
    '''
    def __init__(self):
        pass

    #strings for GUI
    def return_values(self):
        return [b'blank', b'', b'', b'', b'']

    def __call__(self, args):
        return np.zeros([3, 10, 10, 10])
