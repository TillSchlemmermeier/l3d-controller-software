# modules
import numpy as np


class g_blank():
    '''
    Generator: blank
    '''
    def __init__(self):
        pass

    def return_values(self):
        return [['', ''],
				['', ''],
				['', '']]

    def __call__(self, args):
        return np.zeros([3, 10, 10, 10])
