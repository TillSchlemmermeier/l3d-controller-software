# modules
import numpy as np
from scipy.ndimage.interpolation import rotate
from multiprocessing import shared_memory
from random import random, randint, uniform, choice

class e_rotation():

    def __init__(self):
        self.xspeed = 0.1
        self.yspeed = 0.1
        self.zspeed = 0.0
        self.step = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.mode = 'normal'
        self.old_volume = 0
        self.oldspeed = [0.1, 0.1, 0.0]
        self.lastvalue = 0
        self.counter = 0
        self.old_xspeed = self.xspeed
        self.old_yspeed = self.yspeed
        self.old_zspeed = self.zspeed

    def return_state(self):
        return [
            ['X speed', 'xspeed', round(self.xspeed if self.xspeed < 10 else -20 + self.xspeed,1)],
            ['Y speed', 'yspeed', round(self.yspeed if self.yspeed < 10 else -20 + self.yspeed,1)],
            ['Z speed', 'zspeed', round(self.zspeed if self.zspeed < 10 else -20 + self.zspeed,1)],
            ['mode', 'mode', self.mode],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.xspeed = args[0]*20
        self.yspeed = args[1]*20
        self.zspeed = args[2]*20
        self.mode = ['normal', 'fixed', 'trigger'][round(args[3]*2)]
        # === PARAMETERS END ===

        runtime_xspeed = self.xspeed
        runtime_yspeed = self.yspeed
        runtime_zspeed = self.zspeed

        if self.xspeed > 10:
            runtime_xspeed =  - 20 + self.xspeed
        if self.yspeed > 10:
            runtime_yspeed = - 20 + self.yspeed
        if self.zspeed > 10:
            runtime_zspeed = - 20 + self.zspeed

        if self.mode == 'trigger':
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume+1
                self.step = 0
#                self.xspeed = choice([-1,1])*((2-np.log(self.counter))/2) * self.xspeed + self.xspeed
#                self.yspeed = choice([-1,1])*((2-np.log(self.counter))/2) * self.yspeed + self.yspeed
#                self.xspeed = choice([-1,1])*((2-np.log(self.counter))/2) * self.zspeed + self.zspeed
                self.old_xspeed = choice([-1,1])#*self.xspeed #*((2-np.log(self.counter))/2) * self.xspeed + self.xspeed
                self.old_yspeed = choice([-1,1])#*self.yspeed#*((2-np.log(self.counter))/2) * self.yspeed + self.yspeed
                self.old_zspeed = choice([-1,1])#*self.zspeed#*((2-np.log(self.counter))/2) * self.zspeed + self.zspeed

#                self.counter += 1

            runtime_xspeed *= self.old_xspeed
            runtime_yspeed *= self.old_yspeed
            runtime_zspeed *= self.old_zspeed

        # rotate
        for i in range(3):
            world[i, :, :, :] = rotate(world[i, :, :, :], self.step*runtime_xspeed,
                              axes = (1,2), order = 1,
    	                      mode = 'nearest', reshape = False)

            world[i, :, :, :] = rotate(world[i, :, :, :], self.step*runtime_yspeed,
                              axes = (0,1), order = 1,
    	                      mode = 'nearest', reshape = False)

            world[i, :, :, :] = rotate(world[i, :, :, :], self.step*runtime_zspeed,
                              axes = (0,2), order = 1,
    	                      mode = 'nearest', reshape = False)


        world[:, :, :, :] = world[:, :, :, :]**1.3

        if self.mode == 'fixed':
            self.step = 18
        else:
            self.step += 1

        return np.clip(world, 0, 1)
