# modules
import numpy as np
from scipy.signal import sawtooth
from random import randint, choice
from generators.g_genhsphere import gen_hsphere
from multiprocessing import shared_memory


# fortran routine is in g_growing_sphere_f.f90

class g_growingface():
    '''
    Generator: growing_face

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
        self.trigger = False

    #Strings for GUI
    def return_values(self):
        return [b'growingface', b'maxsize', b'speed', b'channel', b'']

    def return_gui_values(self):
        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = 'Trigger'
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.maxsize,2)), str(round(self.growspeed,2)), channel, ''),'utf-8')


    def __call__(self, args):
        self.maxsize = args[0]*17
        self.growspeed = 55 - (args[1]*45+9)
        self.steps = int(self.maxsize/self.growspeed)
        self.channel = int(args[2]*5)-1

    #def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if self.counter == 0:
                list = ([0,4.5,4.5],[9,4.5,4.5],[4.5,0,4.5],[4.5,9,4.5],[4.5,4.5,0],[4.5,4.5,9])
                [self.xpos, self.ypos, self.zpos] = choice(list)
            if current_volume > 0:
                self.counter += 1
                if self.counter > self.growspeed:
                    self.counter = 0

        # check if s2l trigger is activated
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.trigger = True
                self.counter = 0
                list = ([0,4.5,4.5],[9,4.5,4.5],[4.5,0,4.5],[4.5,9,4.5],[4.5,4.5,0],[4.5,4.5,9])
                [self.xpos, self.ypos, self.zpos] = choice(list)

            if self.trigger:
                if self.counter < self.growspeed:
                    self.counter += 1
                else:
                    self.trigger = False

        else:
            # check for new calculation
            if self.counter > self.growspeed:
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

        if self.channel < 0:
            self.counter += 1

        return np.round(np.clip(world, 0, 1), 3)
