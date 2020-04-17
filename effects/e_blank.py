# modules
import numpy as np


class e_blank():
    '''
    Effect: blank
    '''
    def __init__(self):
        pass

    def return_values(self):
        return [['', ''],
				['', ''],
				['', '']]

    def __call__(self, world, args):
        return world
