# modules
import numpy as np
from random import randint, choice
from multiprocessing import shared_memory
from scipy.ndimage.interpolation import rotate

class g_rotating_circle():
    '''
    Generator: kreise halt
    '''

    def __init__(self):
        self.number = 1
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.soundsize = 1
        self.lastvalue = 0
        self.counter = 0
        self.channel = 0
        self.counter_total = 0
        self.mode = 'random'

        self.xspeed = 0
        self.yspeed = 1.0
        self.zspeed = 0
        self.brigthness = 0.5


    #Strings for GUI
    def return_values(self):
        return [b'rotating circle',  b'xpseed', b'yspeed', b'zspeed',b'brightness']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.xspeed,2)), str(round(self.yspeed,2)), str(round(self.zspeed,2)), str(round(self.brightness,2))),'utf-8')


    def __call__(self, args):
        '''
        self.number = int(args[0]*10)
        if args[1] < 0.5:
            self.mode = 'random'
        else:
            self.mode = 'tunnel'
        '''

#        self.channel = int(args[3]*5)-1
        self.xspeed = args[0]*2
        self.yspeed = args[1]*2
        self.zspeed = args[2]*2
        self.brightness = args[3]*0.5+0.5

        # create world
        world1 = np.zeros([3, 10, 10, 10])
        world2 = np.zeros([3, 10, 10, 10])

        '''
        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            self.number = int(10 * current_volume)
            self.soundsize =int(np.clip(3 * current_volume, 0, 3))

        # check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 8

            if self.counter > 0:
                self.number = self.counter
                self.counter -= 1
        '''

        '''
        world[0, 4, 4, 4] = 1
        world[0, 4, 5, 4] = 1
        world[0, 5, 4, 5] = 1
        world[0, 5, 5, 5] = 1
        '''
        '''
        world2[:, 3, 4, 3] = 1
        world2[:, 3, 5, 3] = 1
        world2[:, 6, 4, 6] = 1
        world2[:, 6, 5, 6] = 1
        world2[:, 4, 3, 4] = 1
        world2[:, 4, 6, 4] = 1
        world2[:, 5, 3, 5] = 1
        world2[:, 5, 6, 5] = 1
        '''
        world2[:, 2, 4, 2] = self.brightness
        world2[:, 2, 5, 2] = self.brightness
        world2[:, 7, 4, 7] = self.brightness
        world2[:, 7, 5, 7] = self.brightness
        world2[:, 4, 2, 4] = self.brightness
        world2[:, 4, 7, 4] = self.brightness
        world2[:, 5, 2, 5] = self.brightness
        world2[:, 5, 7, 5] = self.brightness
        world2[:, 3, 3, 3] = self.brightness
        world2[:, 3, 6, 3] = self.brightness
        world2[:, 6, 3, 6] = self.brightness
        world2[:, 6, 6, 6] = self.brightness


        # rotate
        for i in range(3):
            world2[i, :, :, :] = rotate(world2[i, :, :, :], self.counter*self.xspeed,
                              axes = (1,2), order = 1,
    	                      mode = 'nearest', reshape = False)

            world2[i, :, :, :] = rotate(world2[i, :, :, :], self.counter*self.yspeed,
                              axes = (0,1), order = 1,
    	                      mode = 'nearest', reshape = False)

            world2[i, :, :, :] = rotate(world2[i, :, :, :], self.counter*self.zspeed,
                              axes = (0,2), order = 1,
    	                      mode = 'nearest', reshape = False)


        world1[:, 2, 4, 2] = self.brightness
        world1[:, 2, 5, 2] = self.brightness
        world1[:, 7, 4, 7] = self.brightness
        world1[:, 7, 5, 7] = self.brightness
        world1[:, 4, 2, 4] = self.brightness
        world1[:, 4, 7, 4] = self.brightness
        world1[:, 5, 2, 5] = self.brightness
        world1[:, 5, 7, 5] = self.brightness
        world1[:, 3, 3, 3] = self.brightness
        world1[:, 3, 6, 3] = self.brightness
        world1[:, 6, 3, 6] = self.brightness
        world1[:, 6, 6, 6] = self.brightness

        self.counter += 1

        return np.clip(world1+world2, 0, 1)
