# modules
import numpy as np
from scipy.signal import sawtooth
from random import randint, choice
from generators.g_genhsphere import gen_hsphere


# fortran routine is in g_growing_sphere_f.f90

class g_growingface():
    '''
    Generator: growing_face

    a growing hollow sphere from a corner of the cube

    Parameters:
    - maxsize
    - growspeed
    - oscillate y/n
    '''

    def __init__(self):
        self.maxsize = 10
        self.growspeed = 1
        self.steps = 0
        self.counter = 0

        self.xpos = 0
        self.ypos = 0
        self.zpos = 0

    #Strings for GUI
    def return_values(self):
        return [b'growingface', b'maxsize', b'growspeed', b'steps', b'']

    def __call__(self, args):
        self.maxsize = args[0]*18
        self.growspeed = args[1]*50+ 10.0001
        self.steps = int(self.maxsize/self.growspeed)

    #def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])

        # check for new calculation
        if self.counter > self.growspeed:

            #self.xpos = 4.5*randint(0,2)
            #self.ypos = 4.5*randint(0,2)
            #self.zpos = 4.5*randint(0,2)
            list = ([0,4.5,4.5],[9,4.5,4.5],[4.5,0,4.5],[4.5,9,4.5],[4.5,4.5,0],[4.5,4.5,9])
            [self.xpos, self.ypos, self.zpos] = choice(list)


            self.counter = 0

        x = self.xpos
        y = self.ypos
        z = self.zpos

        size = (-np.cos(self.counter*3.14/self.growspeed)+1)*0.5*self.maxsize

        #size = self.maxsize*(-np.cos(self.counter*3.14/self.growspeed)+1)*0.5
        #size = self.maxsize*(np.sin(np.pi*0.5*self.counter/self.growspeed - 0.5*np.pi)+1)

        # creates hollow sphere with parameters
        world[0, :, :, :] = gen_hsphere(size,x,y,z)
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        self.counter += 1

        return np.round(np.clip(world, 0, 1), 3)
