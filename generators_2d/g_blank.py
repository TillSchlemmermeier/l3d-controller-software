# modules
import numpy as np


class g_blank():
    '''
    Generator: blank
    '''
    def __init__(self, resolution):
        self.resolution = resolution
        pass

    #strings for GUI
    def return_values(self):
        return [b'blank', b'', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format('', '', '', ''),'utf-8')

    def __call__(self, args):
        return np.zeros([3, self.resolution[0], self.resolution[1]])
