# modules
import numpy as np
from scipy.ndimage.interpolation import rotate
from multiprocessing import shared_memory
from random import random, randint, uniform

class e_rotation():

    def __init__(self):
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.step = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4
        self.old_volume = 0
        self.oldspeed = [0.1, 0.1, 0.0]

    #strings for GUI
    def return_values(self):
        return [b'rotation', b'X speed', b'Y speed', b'Z speed', b'channel']

    def return_gui_values(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.xspeed,1)), str(round(self.yspeed,1)), str(round(self.zspeed,1)), channel), 'utf-8')

    def __call__(self, world, args):
        self.xspeed = args[0]*20
        self.yspeed = args[1]*20
        self.zspeed = args[2]*20
        self.channel = int(args[3]*4)-1

        if self.xspeed > 10:
            self.xspeed =  - 20 + self.xspeed
        if self.yspeed > 10:
            self.yspeed = - 20 + self.yspeed
        if self.zspeed > 10:
            self.zspeed = - 20 + self.zspeed

        # check if s2l is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            current_volume = np.clip(current_volume, 0, 10)
            if self.old_volume < current_volume:
                self.old_volume = current_volume
                self.step = 0
                amount = [0,0,0]
                amount[0] = 5 * current_volume * uniform(0, 1)
                amount[1] = 5 * (current_volume-amount[0]) * uniform(0, 1)
                amount[2] = 5 * (current_volume-amount[0]-amount[1])

                direction = randint(0,5)

                if direction == 0:
                    self.oldspeed[0] = self.xspeed + amount[0]
                    self.oldspeed[1] = self.yspeed + amount[1]
                    self.oldspeed[2] = self.zspeed + amount[2]

                elif direction == 1:
                    self.oldspeed[0] = self.xspeed + amount[0]
                    self.oldspeed[1] = self.yspeed + amount[2]
                    self.oldspeed[2] = self.zspeed + amount[1]

                elif direction == 2:
                    self.oldspeed[0] = self.xspeed + amount[1]
                    self.oldspeed[1] = self.yspeed + amount[0]
                    self.oldspeed[2] = self.zspeed + amount[2]

                elif direction == 3:
                    self.oldspeed[0] = self.xspeed + amount[1]
                    self.oldspeed[1] = self.yspeed + amount[2]
                    self.oldspeed[2] = self.zspeed + amount[0]

                elif direction == 4:
                    self.oldspeed[0] = self.xspeed + amount[2]
                    self.oldspeed[1] = self.yspeed + amount[0]
                    self.oldspeed[2] = self.zspeed + amount[1]

                elif direction == 5:
                    self.oldspeed[0] = self.xspeed + amount[2]
                    self.oldspeed[1] = self.yspeed + amount[1]
                    self.oldspeed[2] = self.zspeed + amount[0]

#            self.old_volume = np.clip(self.old_volume - 0.08, 0, 100)*0.9
            self.old_volume = np.clip(self.old_volume - current_volume/8, 0, 100)*0.9
            # rotate
            for i in range(3):
                world[i, :, :, :] = rotate(world[i, :, :, :], self.step*self.oldspeed[0],
                                  axes = (1,2), order = 1,
        	                      mode = 'nearest', reshape = False)

                world[i, :, :, :] = rotate(world[i, :, :, :], self.step*self.oldspeed[1],
                                  axes = (0,1), order = 1,
        	                      mode = 'nearest', reshape = False)

                world[i, :, :, :] = rotate(world[i, :, :, :], self.step*self.oldspeed[2],
                                  axes = (0,2), order = 1,
        	                      mode = 'nearest', reshape = False)

        else:
            # rotate
            for i in range(3):
                world[i, :, :, :] = rotate(world[i, :, :, :], self.step*self.xspeed,
                                  axes = (1,2), order = 1,
        	                      mode = 'nearest', reshape = False)

                world[i, :, :, :] = rotate(world[i, :, :, :], self.step*self.yspeed,
                                  axes = (0,1), order = 1,
        	                      mode = 'nearest', reshape = False)

                world[i, :, :, :] = rotate(world[i, :, :, :], self.step*self.zspeed,
                                  axes = (0,2), order = 1,
        	                      mode = 'nearest', reshape = False)


        world[:, :, :, :] = world[:, :, :, :]**1.3
        self.step += 1

        return np.clip(world, 0, 1)
