# modules
import numpy as np
from scipy.signal import sawtooth
from random import randint
from generators.g_genhsphere import gen_hsphere

# fortran routine is in g_growing_sphere_f.f90

class g_growing_corner():
    '''
    Generator: growing_corner

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
        return [b'growing_corner', b'maxsize', b'speed', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.maxsize,2)), str(round(self.growspeed,2)), '', ''),'utf-8')


    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.maxsize = args[0]*18
        self.growspeed = 60 - (args[1]*50+5)
        self.steps = int(self.maxsize/self.growspeed)

        world = np.zeros([3, 10, 10, 10])

        # check for new calculation
        if self.counter > self.growspeed:
            self.xpos = 9*randint(0,1)
            self.ypos = 9*randint(0,1)
            self.zpos = 9*randint(0,1)

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
