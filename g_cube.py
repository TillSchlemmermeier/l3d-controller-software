# modules
import numpy as np


class g_cube():
    '''
    Generator: cube

    a cube in the cube

    Parameters:
    - size
    '''

    def __init__(self):
        self.size = 2

    def control(self, size, blub0, blub1):
        self.size = round(size*4)

    def generate(self, step):
        # create world
        world = np.zeros([3, 10, 10, 10])
        # create smaller world
        tempworld = np.zeros([10, 10, 10])
        tempworld[:, :, :] = 0.0  # -1 for just the cornering lines, needs to be fixed
        size = self.size

        # write cube
        # x slices
        tempworld[4-size, 4-size:6+size, 4-size:6+size] += 1
        tempworld[5+size, 4-size:6+size, 4-size:6+size] += 1
        # y slices
        tempworld[4-size:6+size, 4-size, 4-size:6+size] += 1
        tempworld[4-size:6+size, 5+size, 4-size:6+size] += 1
        # z slices
        tempworld[4-size:6+size, 4-size:6+size, 4-size] += 1
        tempworld[4-size:6+size, 4-size:6+size, 5+size] += 1

        # path world together
        world[0, :, :, :] = tempworld
        world[1, :, :, :] = tempworld
        world[2, :, :, :] = tempworld

        return np.clip(world, 0, 1)
