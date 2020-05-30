# modules
import numpy as np


class g_grid():
    '''
    Generator: grid
    a 3D grid
    Parameters:
    - step
    '''

    def __init__(self):
        self.stepX = 2
        self.stepY = 2
        self.stepZ = 2

    #Strings for GUI
    def return_values(self):
        return [b'grid', b'stepX', b'stepY', b'stepZ', b'']

    def __call__(self, args):
        self.stepX = round(args[0]*9)+1
        self.stepY = round(args[1]*9)+1
        self.stepZ = round(args[2]*9)+1

        # create world
        world = np.zeros([3, 10, 10, 10])

        for x in range(9):
            for y in range(9):
                for z in range(9):
                    if x%self.stepX == 0 or y%self.stepY == 0 or z%self.stepZ == 0:
                        world[:, x, y, z] = 1.0

        return np.clip(world, 0, 1)
