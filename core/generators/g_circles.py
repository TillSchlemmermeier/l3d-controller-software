# modules
import struct
import numpy as np
from random import randint, choice
from multiprocessing import shared_memory

class g_circles():
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

        # size 5
        self.size5 = np.zeros([10,10])

        # straight
        self.size5[0,3:7] = 1.0
        self.size5[9,3:7] = 1.0
        self.size5[3:7,0] = 1.0
        self.size5[3:7,9] = 1.0

        # diag
        self.size5[1,2] = 1.0
        self.size5[2,1] = 1.0

        self.size5[1,7] = 1.0
        self.size5[2,8] = 1.0

        self.size5[7,1] = 1.0
        self.size5[8,2] = 1.0

        self.size5[7,8] = 1.0
        self.size5[8,7] = 1.0


        # size 4
        self.size4 = np.zeros([10,10])

        # straight
        self.size4[1,3:7] = 1.0
        self.size4[8,3:7] = 1.0
        self.size4[3:7,1] = 1.0
        self.size4[3:7,8] = 1.0

        # diag
        self.size4[2,2] = 1.0
        self.size4[2,7] = 1.0
        self.size4[7,2] = 1.0
        self.size4[7,7] = 1.0

        # size 3
        self.size3 = np.zeros([10,10])

        # straight
        self.size3[2,3:7] = 1.0
        self.size3[7,3:7] = 1.0
        self.size3[3:7,2] = 1.0
        self.size3[3:7,7] = 1.0

        # size 2
        self.size2 = np.zeros([10,10])

        # straight
        self.size2[3,4:6] = 1.0
        self.size2[6,4:6] = 1.0
        self.size2[4:6,3] = 1.0
        self.size2[4:6,6] = 1.0

    def return_state(self):
        return [
            ['number', 'number', round(self.number,2)],
            ['mode', 'mode', self.mode],
            ['channel', 'channel', self.channel],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.number = int(args[0]*10)
        self.mode = ['random', 'tunnel'][round(args[1])]
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[2]*5)]
        # === PARAMETERS END ===

        # create world
        world = np.zeros([3, 10, 10, 10])

        runtime_number = self.number

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            runtime_number = int(10 * current_volume)
            self.soundsize =int(np.clip(3 * current_volume, 0, 3))

        # check for trigger
        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 8

            if self.counter > 0:
                runtime_number = self.counter
                self.counter -= 1


        for i in range(runtime_number):
            # check if S2L is activated
            if isinstance(self.channel, int):
                j = int(np.clip(randint(self.soundsize - 1, self.soundsize + 1), 0, 3))
            else:
                j = randint(0,3)

            if self.mode == 'random':
                if j == 0:
                    world[0, :, randint(0,9), :] = self.size2[:,:]

                elif j == 1:
                    world[0, :, randint(0,9), :] = self.size3[:,:]

                elif j == 2:
                    world[0, :, randint(0,9), :] = self.size4[:,:]

                elif j == 3:
                    world[0, :, randint(0,9), :] = self.size5[:,:]
            elif self.mode == 'tunnel':
                pos = (self.counter_total - i) % 10  # Offset position by loop index
                world[0, :, int(pos), :] = self.size4[:,:]

        # rotate if necessary
        world[0, :, :, :] = np.rot90(world[0, :, :, :], k = 1)

        world[1,:,:,:] = world[0, :, : , :]
        world[2,:,:,:] = world[0, :, : , :]

        self.counter_total += 1

        return np.clip(world, 0, 1)
