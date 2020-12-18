import numpy as np
import scipy
from random import randint
from multiprocessing import shared_memory

class g_inandout:
    def __init__(self):
        self.number = 1
        self.fadespeed = 0.1
        self.leds = []

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    #Strings for GUI
    def return_values(self):
        return [b'inandout', b'number', b'fade in', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number,2)), str(round(self.fadespeed,2)), '', channel),'utf-8')


    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.number = int(args[0]*10+1)
        self.fadespeed = 0.5*args[1]+0.01
        self.channel = int(args[3]*4)-1

        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                self.fadespeed = np.clip(current_volume / 2, 0, 0.5)
                self.leds.append(led(self.fadespeed))

        # check for new leds
        elif len(self.leds) < self.number:
            self.leds.append(led(self.fadespeed))

        delete_index = -1
        # turn on leds
        for i in range(len(self.leds)):
            temp = self.leds[i]()
            if temp[0] < 2:
                world[:, temp[1], temp[2], temp[3]] = temp[4]
            else:
                delete_index = i

        # check for delete
        if delete_index != -1:
            del self.leds[delete_index]

        return np.clip(world, 0, 1)**2

class led:
    def __init__(self, fadespeed):
        self.x,self.y,self.z = randint(0,9), randint(2,7), randint(2,7)
        self.fadespeed = fadespeed
        self.brightness = 0
        self.state = 0
        self.dx, self.dy, self.dz = 0, 0, 0

        if randint(0, 1) == 1:
            # figure out direction
            if self.z >= 4:
                self.dz = -1
            else:
                self.dz = 1
        else:
            if self.y >= 4:
                self.dy = -1
            else:
                self.dy = 1

    def __call__(self):
        # perform action
        if self.state == 0:
            self.brightness += self.fadespeed
        elif self.state == 1:
            #self.x += self.dx
            self.y += self.dy
            self.z += self.dz

        output = [self.state,
                  np.clip(self.x,0,9),
                  np.clip(self.y,0,9),
                  np.clip(self.z,0,9),
                  np.clip(self.brightness,0,1)]

        # check for state
        if self.state == 0 and self.brightness > 1.0:
            self.state = 1
        elif self.state == 1 and (self.x < 0 or self.x > 9 or self.y < 0 or self.y > 9 or self.z < 0 or self.z > 9):
            self.state = 2

        return output
