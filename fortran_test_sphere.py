# modules
import numpy as np
from random import randint
from g_sphere_f_helper import gen_sphere

class fortran_test_sphere():
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

    def label(self):
        return ['size',round(self.size,2),'empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])

        posx = randint(0,9)
        posy = randint(0,9)
        posz = randint(0,9)

        world[0,:,:,:] = gen_sphere(self.size, posx, posy, posz)

        return np.clip(world, 0, 1)
