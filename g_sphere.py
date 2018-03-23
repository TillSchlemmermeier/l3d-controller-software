# modules
import numpy as np
from random import randint


class g_sphere():
    '''
    Generator: sphere

    sphere at a random position

    Parameters:
    - size
    '''
    def __init__(self):
        self.size = 2
        self.color = 0

    def control(self, color, size, blub0):
        self.size = round(size*10)
        # self.color = round(color*2)

    def generate(self, step):

        world = np.zeros([3, 10, 10, 10])

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    dist = np.sqrt((x-randint(0, 9))**2+(y-randint(0, 9))**2+(z-randint(0, 9))**2)
                    if dist <= self.size:
                        world[:, x, y, z] = 1.0

        return np.clip(world, 0, 1)
