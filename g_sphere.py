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

    def control(self, size, blub0, blub1):
        self.size = round(size*10)

    def label(self):
        return ['size',self.size,'empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])

        posx = randint(0,9)
        posy = randint(0,9)
        posz = randint(0,9)

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    dist = np.sqrt((x-posx)**2+(y-posy)**2+(z-posz)**2)
                    if dist <= self.size:
                        world[:, x, y, z] = 1.0

        return np.clip(world, 0, 1)
