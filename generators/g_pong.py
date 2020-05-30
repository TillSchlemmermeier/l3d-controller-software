# modules
import numpy as np
from random import randint, uniform
from generators.g_sphere_f import gen_sphere

# fortran routine is in g_sphere_f.f90

class g_pong():

    def __init__(self):
        self.speed = 1.0
        self.size = 1.0

        # generate initial position and velocity
        self.pos = [uniform(-3, 3)+4.5, uniform(-3, 3)+4.5, uniform(-3, 3)+4.5]
        self.vec = [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)]

    #Strings for GUI
    def return_values(self):
        return [b'sphere', b'speed', b'', b'', b'']

    def __call__(self, args):
        self.speed = round(args[0]*4)

        world = np.zeros([3, 10, 10, 10])

        # propagate
        newpos = self.pos + self.speed*self.vec
        self.pos = newpos

        # draw new point
        world[0,:,:,:] = gen_sphere(self.size, *self.pos)

        # check for collision
        if newpos[0] > 9:
            self.vec[0] *= -1
            world[0, 9, :, :] +=  gen_sphere(self.size*2, *self.pos)[9, :, :]
        elif newpos[0] < 0:
            self.vec[0] *= -1
            world[0, 0, :, :] +=  gen_sphere(self.size*2, *self.pos)[0, :, :]
        elif newpos[1] > 9:
            self.vec[1] *= -1
            world[0, :, 0, :] +=  gen_sphere(self.size*2, *self.pos)[:, 9, :]
        elif newpos[1] < 0:
            self.vec[1] *= -1
            world[0, :, 9, :] +=  gen_sphere(self.size*2, *self.pos)[:, 0, :]
        elif newpos[2] > 9:
            self.vec[2] *= -1
            world[0, :, 0, :] +=  gen_sphere(self.size*2, *self.pos)[:, :, 9]
        elif newpos[2] < 0:
            self.vec[2] *= -1
            world[0, :, 9, :] +=  gen_sphere(self.size*2, *self.pos)[:, :, 0]

        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        return np.clip(world, 0, 1)
