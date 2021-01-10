# modules
import numpy as np
from scipy.signal import sawtooth
from random import randint, choice
from generators.g_genhsphere import gen_hsphere
from multiprocessing import shared_memory

# fortran routine is in g_growing_sphere_f.f90

class g_growing_corner():
    '''
    Generator: growing_corner

    a growing hollow sphere from a corner of the cube

    Parameters:
    - maxsize
    - growspeed
    - oscillate y/n
    - s2l channel
    '''

    def __init__(self):
        self.maxsize = 10
        self.growspeed = 1
        self.steps = 0
        self.counter = 0

        self.xpos = 0
        self.ypos = 0
        self.zpos = 0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4
        self.lastvalue = 0

    #Strings for GUI
    def return_values(self):
        return [b'growing_corner', b'maxsize', b'speed', b'', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.maxsize,2)), str(round(self.growspeed,2)), '', channel),'utf-8')


    def __call__(self, args):
        self.maxsize = args[0]*18
        self.growspeed = 60 - (args[1]*50+5)
        self.steps = int(self.maxsize/self.growspeed)
        self.channel = int(args[3]*5)-1

        world = np.zeros([3, 10, 10, 10])

        # check for new calculation
        if self.counter > self.growspeed:
            self.xpos = 9*randint(0,1)
            self.ypos = 9*randint(0,1)
            self.zpos = 9*randint(0,1)

            self.counter = 0

        # check if s2l is activated
        elif 4 > self.channel >= 0:
            if self.counter == 0:
                list = ([0,0,0],[0,0,9],[0,9,0],[0,9,9],[9,0,0],[9,9,0],[9,0,9], [9,9,9])
                [self.xpos, self.ypos, self.zpos] = choice(list)
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                self.counter += int(current_volume*2)
                if self.counter > self.maxsize:
                    self.counter = 0
        #check for trigger
        elif self.channel == 4:
            if self.counter == 0:
                list = ([0,0,0],[0,0,9],[0,9,0],[0,9,9],[9,0,0],[9,9,0],[9,0,9], [9,9,9])
                [self.xpos, self.ypos, self.zpos] = choice(list)
            current_volume = int(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0
            else:
                self.counter += 1
                #if self.counter > self.maxsize:
                #    self.counter = 0

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

        if self.channel < 0:
            self.counter += 1

        return np.round(np.clip(world, 0, 1), 3)
