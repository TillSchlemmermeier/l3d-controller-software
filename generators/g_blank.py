# modules
import numpy as np


class g_blank():
    '''
    Generator: blank
    '''
    def __init__(self):
        #print('g_blank is set!')
        self.message = 'g_blank renders frame!'

    def control(self, args):
        print('g_blank gets parameters!')

    def generate(self, step):
        print(self.message)
        return np.zeros([3, 10, 10, 10])
