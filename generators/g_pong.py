# modules
import numpy as np
from random import randint, uniform
#from generators.g_sphere_f import gen_sphere
from generators.gen_central_glow_f import gen_central_glow

# fortran routine is in g_sphere_f.f90

class g_pong():

    def __init__(self):
        self.speed = 1.0
        self.size = 4.0
        self.side_size = 2.0
        self.reset_frame = 50
        self.counter = 0

        # generate initial position and velocity
        self.pos = np.array([uniform(-3, 3)+4.5, uniform(-3, 3)+4.5, uniform(-3, 3)+4.5])
        self.vec = np.array([uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)])
        #self.vec = np.array([0,0,0.5])
        #self.pos = np.array([4,4,4])
    #Strings for GUI
    def return_values(self):
        return [b'sphere', b'speed', b'size', b'side size', b'reset']

    def __call__(self, args):
        self.speed = (args[0]+0.01)*2
        self.size = (args[1]+0.01)*10
        self.side_size = (args[2]+0.01)*6
        self.reset_frame = (args[3]+10)*10

        world = np.zeros([3, 10, 10, 10])

        # propagate
        newpos = self.pos + self.speed*self.vec
        self.pos = newpos

        # draw new point
        world[0,:,:,:] = gen_central_glow(self.size, *self.pos)

        # check for collision
        if newpos[0] > 9:
            self.vec[0] *= -1
            world[0, 9, :, :] += gen_central_glow(self.side_size, *self.pos)[9, :, :]
        elif newpos[0] < 0:
            self.vec[0] *= -1
            world[0, 0, :, :] += gen_central_glow(self.side_size, *self.pos)[0, :, :]

        if newpos[1] > 9:
            self.vec[1] *= -1
            world[0, :, 9, :] += gen_central_glow(self.side_size, *self.pos)[:, 9, :]
        elif newpos[1] < 0:
            self.vec[1] *= -1
            world[0, :, 0, :] += gen_central_glow(self.side_size, *self.pos)[:, 0, :]

        if newpos[2] > 9:
            self.vec[2] *= -1
            world[0, :, :, 9] += gen_central_glow(self.side_size, *self.pos)[:, :, 9]
        elif newpos[2] < 0:
            self.vec[2] *= -1
            world[0, :, :, 0] += gen_central_glow(self.side_size, *self.pos)[:, :, 0]

        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        if self.counter > self.reset_frame:
            self.pos = np.array([uniform(-3, 3)+4.5, uniform(-3, 3)+4.5, uniform(-3, 3)+4.5])
            self.vec = np.array([uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)])
            self.counter = 0

        self.counter += 1
        
        return np.clip(world, 0, 1)
