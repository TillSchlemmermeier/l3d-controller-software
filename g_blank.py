# modules
import numpy as np


class g_blank():
    '''
    Generator: blank

    '''

    def __init__(self):
        self.dummy = 0

    def control(self, dummy0, dummy1, dummy2):
        self.dummy = dummy0

    def generate(self, step, dumpworld):
        return np.zeros([3,10,10,10])
