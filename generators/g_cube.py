# modules
import numpy as np


class g_cube():
    '''
    Generator: cube
    a cube in the cube
    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    '''

    def __init__(self):
        self.size = 4
        self.sides = False

    #Strings for GUI
    def return_values(self):
        return [b'cube', b'size', b'sides (Off / On)', b'', b'']

    def __call__(self, args):
        self.size = round(args[0]*4)
        if args[1] < 0.5:
            self.sides = False
        else:
            self.sides = True

        # create world
        world = np.zeros([3, 10, 10, 10])
        # create smaller world
        tempworld = np.zeros([10, 10, 10])

        if not self.sides:
            tempworld[:, :, :] = -1.0

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
