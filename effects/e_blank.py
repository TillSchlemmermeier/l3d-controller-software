# modules
import numpy as np


class e_blank():
    '''
    Effect: blank
    '''
    def __init__(self):
        self.message = 'e_blank renders frame!'

    def control(self, args):
        print('e_blank gets parameters!')

    def generate(self, step, world):
        print(self.message)
        return np.zeros([3, 10, 10, 10])
