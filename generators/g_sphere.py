# modules
import numpy as np
from random import randint
from generators.g_sphere_f import gen_sphere

# fortran routine is in g_sphere_f.f90

class g_sphere():

    def __init__(self):
        self.size = 2
        self.color = 0

    def return_values():
        pass#return {'Number of LEDs', self.number_of_leds}

    def __call__(self, args):
        self.size = round(args[0]*10)

        world = np.zeros([3, 10, 10, 10])

        posx = randint(0,9)
        posy = randint(0,9)
        posz = randint(0,9)

        world[0,:,:,:] = gen_sphere(self.size, posx, posy, posz)
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        return np.clip(world, 0, 1)
