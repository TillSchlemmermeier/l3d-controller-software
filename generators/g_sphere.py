# modules
import numpy as np
from random import randint
from generators.g_sphere_f import gen_sphere

# fortran routine is in g_sphere_f.f90

class g_sphere():

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
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        return np.clip(world, 0, 1)
