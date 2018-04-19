# modules
import numpy as np


class e_blank():
    '''
    Effect: blank
    '''

    def __init__(self):
        self.dummy = 0.0

    def control(self, blub0, blub1, blub2):
        self.dummy = blub0

    def generate(self, step, world):

        return world
