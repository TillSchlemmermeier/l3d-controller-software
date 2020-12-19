# modules
import numpy as np
from random import randint
from multiprocessing import shared_memory

class g_rain():
    '''
    Generator: cube

    a cube in the cube

    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    '''

    def __init__(self):
        self.numbers = 1
        self.fade = 0.5
        self.lastworld = np.zeros([10, 10, 10])
        self.direction = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    #Strings for GUI
    def return_values(self):
        return [b'rain', b'number', b'fade', b'direction', b'channel']

    def return_gui_values(self):
        if self.direction == 0:
            dir = 'down'
        else:
            dir = "up"

        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.numbers,2)), str(round(self.fade,2)), dir, channel),'utf-8')


    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.numbers = int(args[0]*10 + 1)
        self.fade = args[1]
        self.direction = round(args[2])
        self.channel = int(args[3]*4)-1

        # create world
        world = np.zeros([3, 10, 10, 10])

        # move last world 1 step down
        if self.direction == 0:
            self.lastworld = np.roll(self.lastworld, axis = 0, shift=1)
            self.lastworld[ 0, :, :] = 0.0

            # check if S2L is activated
            if self.channel >= 0:
                current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
                self.numbers = int(10 * current_volume)

            # turn on random leds in upper level
            for i in range(self.numbers):
                world[0,0,randint(0, 9),randint(0, 9)] = 1.0

        else:
            self.lastworld = np.roll(self.lastworld, axis = 0, shift=-1)
            self.lastworld[ 9, :, :] = 0.0

            # check if S2L is activated
            if self.channel >= 0:
                current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
                self.numbers = int(10 * current_volume)

            # turn on random leds in lower level
            for i in range(self.numbers):
                world[0,9,randint(0, 9),randint(0, 9)] = 1.0

        # add last frame
        world[0,:,:,:] += self.lastworld *self.fade
        self.lastworld[:,:,:] = world[0,:,:,:]

        # copy to other colors
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        return np.clip(world, 0, 1)
