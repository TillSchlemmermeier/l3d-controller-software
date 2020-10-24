# modules
import numpy as np
from random import randint
from scipy.stats import multivariate_normal
from multiprocessing import shared_memory

class g_wave():
    '''
    Generator: wave
    A 2D wave coming from a random corner

    Parameters:
    Sigma (width of the wave)
    Speed
    Sound2Light channel
    '''

    def __init__(self):
        self.sigma = 1
        self.speed = 1
        self.counter = 0
        self.direction = 0
        self.position = 1
        self.maxsize = 35
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    #Strings for GUI
    def return_values(self):
        return [b'wave', b'sigma', b'speed', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.sigma,2)), str(round(self.speed,2)), '', channel),'utf-8')

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.sigma = args[0]*1.4+0.2
        self.speed = args[1]*2.5+0.4
        self.channel = int(args[3]*4)-1

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.sigma = current_volume * 1.4 + 0.2

        world = np.zeros([3, 10, 10, 10])

        a = np.zeros([10,10])

        if self.counter > self.maxsize:

            self.direction = randint(1,8)
            self.position = randint(0,9)
            self.counter = 0

            if self.direction < 5:
                self.maxsize=20
            else:
                self.maxsize=31

        i = self.counter
        direction = self.direction
        position = self.position

        if direction == 1: #x+
            for x in range(10):
    #            a[x,:] = ((np.sin((i)/np.pi + x/np.pi)+1)/2)**4
                a[x,:] = np.exp(-(((x+5-i)/self.sigma)**2)/10)
            self.counter -= 0.3
            world[0,position,:,:] = a
        elif direction == 2: #x-
            for x in range(10):
                a[x,:] = np.exp(-(((x-15+i)/self.sigma)**2)/10)
            self.counter -= 0.3
            world[0,position,:,:] = a
        elif direction == 3: #y+
            for y in range(10):
                a[:,y] = np.exp(-(((y+5-i)/self.sigma)**2)/10)
            self.counter -= 0.3
            world[0,position,:,:] = a
        elif direction == 4: #y-
            for y in range(10):
                a[:,y] = np.exp(-(((y-15+i)/self.sigma)**2)/10)
            self.counter -= 0.3
            world[0,position,:,:] = a
        elif direction == 5: #xy
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-(((x+y-25+i)/self.sigma)**2)/10) # done
            world[0,position,:,:] = a
        elif direction == 6: #x-y
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-(((x-y+15-i)/self.sigma)**2)/10) # done
            world[0,position,:,:] = a
        elif direction == 7: #-xy
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-(((-x+y+15-i)/self.sigma)**2)/10)
            world[0,position,:,:] = a
        elif direction == 8: #-x-y
            for x in range(10):
                for y in range(10):
                    a[x,y] = np.exp(-(((-x-y+25-i)/self.sigma)**2)/10)
            world[0,position,:,:] = a

        world[1,:,:,:]=world[0,:,:,:]
        world[2,:,:,:]=world[0,:,:,:]

        self.counter += self.speed


        return np.clip(world, 0, 1)
