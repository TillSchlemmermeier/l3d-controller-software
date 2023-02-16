
import numpy as np
from multiprocessing import shared_memory
from random import choice

class e_roll():


    def __init__(self):
        # parameters
        self.amount = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.counter = 4
        self.direction = choice([-1, 1])
        self.axis = choice([1,2,3])
        self.lastvalue = 0
        self.freq = 1
        self.keep = True
        self.maxcounter = 4

    def return_values(self):
        # strings for GUI
        return [b'roll', b'freq', b'keep old', b'n frames', b'']

    def return_gui_values(self):
        if self.keep:
            keep = 'True'
        else:
            keep = 'False'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.freq,0)), keep, str(round(self.maxcounter,0)), '') ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        self.freq = int(args[0]*10+1)
        if args[1] > 0.5:
            self.keep = True
        else:
            self.keep = False

        self.maxcounter = int(args[2]*10+1)

        current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))

        if current_volume > self.lastvalue:
            self.lastvalue = current_volume+self.freq
            self.counter = self.maxcounter
            self.direction = choice([-1, 1])
            self.axis = choice([1,2,3])

        if self.counter > 0:
            if self.keep:
                world += np.roll(world, shift = int(self.direction*(self.maxcounter-self.counter)), axis = self.axis)
            else:
                self.oldworld = np.roll(world, shift = int(self.direction*(self.maxcounter-self.counter)), axis = self.axis)
                world = self.oldworld


            self.counter -= 1

        return np.clip(world, 0, 1)
