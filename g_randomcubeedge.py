# modules
import numpy as np


class g_randomcubeedge():
    '''
    Generator: cube

    a cube in the cube

    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    '''

    def __init__(self):
        self.size = 2

    def control(self, size, sides, blub1):
        self.size = round(size*4)

    def label(self):
        return ['size',round(self.size,2),'empty','empty','empty','empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        

        return np.clip(world, 0, 1)
