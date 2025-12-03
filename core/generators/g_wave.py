# modules
import struct
import numpy as np
from random import randint
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
        self.lastvalue = 0

    def return_state(self):
        return [
            ['sigma', 'sigma', round(self.sigma,2)],
            ['speed', 'speed', round(self.speed,2)],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.sigma = args[0]*1.4+0.2
        self.speed = args[1]*2.5+0.4
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[2]*5)]
        # === PARAMETERS END ===

        runtime_speed = self.speed

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            self.sigma = current_volume * 1.4 + 0.2

        #check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0
                self.direction = randint(1,8)
                self.position = randint(0,9)

                if self.direction < 5:
                    self.maxsize=20
                else:
                    self.maxsize=31

                if self.counter > self.maxsize:
                    self.counter = self.maxsize


        elif self.counter > self.maxsize:

            self.direction = randint(1,8)
            self.position = randint(0,9)
            self.counter = 0

            if self.direction < 5:
                self.maxsize=20
            else:
                self.maxsize=31


        world = np.zeros([3, 10, 10, 10])

        a = np.zeros([10,10])

        i = self.counter
        direction = self.direction
        position = self.position

        # factor to account for different corner/face speeds
        if direction < 5:
            runtime_speed /= 1.44


        if direction == 1: #x+
            for x in range(10):
    #            a[x,:] = ((np.sin((i)/np.pi + x/np.pi)+1)/2)**4
                a[x,:] = np.exp(-(((x+5-i)/self.sigma)**2)/10)
            world[0,position,:,:] = a
        elif direction == 2: #x-
            for x in range(10):
                a[x,:] = np.exp(-(((x-15+i)/self.sigma)**2)/10)
            world[0,position,:,:] = a
        elif direction == 3: #y+
            for y in range(10):
                a[:,y] = np.exp(-(((y+5-i)/self.sigma)**2)/10)
            world[0,position,:,:] = a
        elif direction == 4: #y-
            for y in range(10):
                a[:,y] = np.exp(-(((y-15+i)/self.sigma)**2)/10)
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


        self.counter += runtime_speed


        return np.clip(world, 0, 1)
