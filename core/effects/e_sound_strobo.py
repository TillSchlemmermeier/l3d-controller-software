import struct
from multiprocessing import shared_memory
import numpy as np

class e_sound_strobo():

    def __init__(self):
        # parameters
        self.channel = 1
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.counter = 0
        self.lastvalue = 0
        self.mode = 'normal'
        self.amount = 1

    def return_state(self):
        return [
            ['amount', 'amount', round(self.amount,1)],
            ['mode', 'mode', self.mode],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount = int(args[0]*12)
        self.mode = ['normal', 'invert'][round(args[1])]
        self.channel = [0, 1, 2, 3, 'Trigger'][round(args[2]*4)]
        # === PARAMETERS END ===

        # apply manipulation
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]**4
            if current_volume > 0.5:
                if self.counter == 0:
                    world[:, :, :, :] = 0
                    self.counter += 1
                else:
                    self.counter = 0
        else:
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.counter = 0


            if self.mode == 'normal':
                if self.counter < self.amount:
                    if self.counter % 2 == 0:
                        world[:, :, :, :] = 0
                    self.counter += 1
                else:
                    self.counter += 1
            else:
                if self.counter < self.amount:
                    if self.counter % 2 != 0:
                        world[:, :, :, :] = 0
                    self.counter += 1
                else:
                    world[:, :, :, :] = 0
                    self.counter += 1


            self.lastvalue = current_volume


        return np.clip(world, 0, 1)
