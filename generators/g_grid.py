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

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    if x%self.stepX == 0 and y%self.stepY == 0:
                        world[:, x, y, :] = 1.0
                    if y%self.stepY == 0 and z%self.stepZ == 0:
                        world[:, :, y, z] = 1.0
                    if z%self.stepZ == 0 and x%self.stepX == 0:
                        world[:, x, :, z] = 1.0

        return np.clip(world, 0, 1)
