# modules
import numpy as np
from random import randint

class g_sides():

    def __init__(self):
        self.size = 4
        self.sides = True

    #Strings for GUI
    def return_values(self):
        return [b'cube', b'size', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.size,2)), '', '', ''),'utf-8')


    def __call__(self, args):
        self.size = round(args[0]*4)

        # create world
        world = np.zeros([3, 10, 10, 10])
        # create smaller world
        tempworld = np.zeros([10, 10, 10])

        if not self.sides:
            tempworld[:, :, :] = -1.0

        size = self.size

        # select side
        side = randint(0, 5)

        if side == 0:
            tempworld[4-size, 4-size:6+size, 4-size:6+size] += 1
        elif side == 1:
            tempworld[5+size, 4-size:6+size, 4-size:6+size] += 1
        elif side == 2:
            tempworld[4-size:6+size, 4-size, 4-size:6+size] += 1
        elif side == 3:
            tempworld[4-size:6+size, 5+size, 4-size:6+size] += 1
        elif side == 4:
            tempworld[4-size:6+size, 4-size:6+size, 4-size] += 1
        elif side == 5:
            tempworld[4-size:6+size, 4-size:6+size, 5+size] += 1

        # path world together
        world[0, :, :, :] = tempworld
        world[1, :, :, :] = tempworld
        world[2, :, :, :] = tempworld

        return np.clip(world, 0, 1)
