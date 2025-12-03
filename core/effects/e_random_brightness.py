# modules
import struct
import numpy as np
from random import uniform
from multiprocessing import shared_memory

class e_random_brightness():

    def __init__(self):
        self.speed = 1
        self.brightness = uniform(0,1)
        self.step = 0
        self.trigger = False
        self.lastvalue = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def return_state(self):
        return [
            ['speed', 'speed', round(11 - self.speed,1)],
            ['trigger', 'trigger', str(self.trigger)],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.speed = 11 - int(args[0]*10)
        self.trigger = args[1] > 0.1
        # === PARAMETERS END ===

        if self.trigger:
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.brightness = uniform(0, 1)

        elif self.step % self.speed == 0:
            self.brightness = uniform(0, 1)

        self.step += 1

        return np.clip(world*self.brightness, 0, 1)
