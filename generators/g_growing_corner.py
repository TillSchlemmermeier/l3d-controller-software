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
        self.lastvalue = 0
        self.trigger = False
        self.switch = False
        self.mode = 'single'

    #Strings for GUI
    def return_values(self):
        return [b'growing_corner', b'maxsize', b'speed', b'mode', b'Trigger']

    def return_gui_values(self):
        if self.trigger:
            trigger = 'On'
        else:
            trigger = 'Off'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.maxsize,2)), str(round(55-self.growspeed,2)), self.mode, trigger),'utf-8')


    def __call__(self, args):
        self.maxsize = args[0]*18
        self.growspeed = 60 - (args[1]*50+5)
        self.steps = int(self.maxsize/self.growspeed)

        if args[3] < 0.5:
            self.trigger = False
        else:
            self.trigger = True

        if args[2] < 0.5:
            self.mode = 'single'
        else:
            self.mode = 'double'

        world = np.zeros([3, 10, 10, 10])

        size = (-np.cos(self.counter*np.pi/self.growspeed)+1)*0.5*self.maxsize


        #check for trigger
        if self.trigger:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.switch = True
                self.counter = 0
                list = ([0,0,0],[0,0,9],[0,9,0],[0,9,9],[9,0,0],[9,9,0],[9,0,9], [9,9,9])
                [self.xpos, self.ypos, self.zpos] = choice(list)

            if self.switch:
                if self.counter < self.growspeed:
                    self.counter += 1
                else:
                    self.switch = False


        elif self.counter > self.growspeed:
            self.xpos = 9*randint(0,1)
            self.ypos = 9*randint(0,1)
            self.zpos = 9*randint(0,1)

            self.counter = 0

        else:
            pass

        x = self.xpos
        y = self.ypos
        z = self.zpos

        #size = self.maxsize*(-np.cos(self.counter*3.14/self.growspeed)+1)*0.5
        #size = self.maxsize*(np.sin(np.pi*0.5*self.counter/self.growspeed - 0.5*np.pi)+1)

        # creates hollow sphere with parameters

        world[0, :, :, :] = gen_hsphere(size,x,y,z)

        if self.mode == 'double':
            world[0, :, :, :] += gen_hsphere(size*2.5,x,y,z)        
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        if not self.trigger:
            self.counter += 1

        return np.round(np.clip(world, 0, 1), 3)
