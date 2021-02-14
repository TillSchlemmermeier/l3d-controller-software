# modules
import numpy as np
from scipy.ndimage.interpolation import rotate
from multiprocessing import shared_memory
from random import randint

class g_rotate_plane():
    def __init__(self):
        self.original = np.zeros([10,10,10])
        for i in range(8):
            self.original[4:5, 1:-1, 1:-1] = 1

        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.step = 0
        self.axe = 0

        self.real_xspeed = 0
        self.real_yspeed = 0
        self.real_zspeed = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.counter = 0

    #Strings for GUI
    def return_values(self):
        return [b'rotate_plane', b'xspeed', b'yspeed', b'zspeed', b'channel']


    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.xspeed,2)), str(round(self.yspeed,2)), str(round(self.zspeed,2)), channel),'utf-8')


    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.xspeed = 20*args[0]
        self.yspeed = 20*args[1]
        self.zspeed = 20*args[2]
        self.channel = int(args[3]*5)-1

        # create world
        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                self.axe = randint(0, 3)
                if self.axe == 0:
                    self.real_xspeed += 20*current_volume
                if self.axe == 1:
                    self.real_yspeed += 20*current_volume
                if self.axe == 2:
                    self.real_zspeed += 20*current_volume

        #check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.axe = randint(0, 3)
                self.counter = 20

            if self.counter > 0:
                if self.axe == 0:
                    self.real_xspeed += self.counter
                if self.axe == 1:
                    self.real_yspeed += self.counter
                if self.axe == 2:
                    self.real_zspeed += self.counter
                self.counter -= 1

        else:
            self.real_xspeed = self.step*self.xspeed
            self.real_yspeed = self.step*self.yspeed
            self.real_zspeed = self.step*self.zspeed
            self.step += 1


        # rotate
        newworld = rotate(self.original, self.real_xspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.real_yspeed,
                          axes = (0,1), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.real_zspeed,
                          axes = (0,2), order = 1,
	                      mode = 'nearest', reshape = False)

        # insert array
        world[0, :, :, :] = newworld
        world[1, :, :, :] = newworld
        world[2, :, :, :] = newworld



        return np.clip(world, 0, 1)
