import struct
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

    def return_state(self):
        return [
            ['freq', 'freq', round(self.freq,0)],
            ['keep old', 'keep', str(self.keep)],
            ['n frames', 'maxcounter', round(self.maxcounter,0)],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.freq = int(args[0]*10+1)
        self.keep = args[1] > 0.5
        self.maxcounter = int(args[2]*10+1)
        # === PARAMETERS END ===

        current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]

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
