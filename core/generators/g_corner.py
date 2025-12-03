import struct
import numpy as np
from colorsys import hsv_to_rgb
from random import uniform
from multiprocessing import shared_memory

class g_corner():
    '''
    Generator: corner
    '''

    def __init__(self):
        self.size = 0
        self.colorlist = []
        self.randomcolor = False
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.counter = 0

    def return_state(self):
        return [
            ['size', 'size', round(self.size,2)],
            ['color', 'randomcolor', 'on' if self.randomcolor else 'off'],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.size = int(args[0]*3 + 1)
        self.randomcolor = args[1] > 0.5
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[2]*5)]
        # === PARAMETERS END ===

        # create world
        world = np.zeros([3, 10, 10, 10])

        runtime_size = self.size

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            runtime_size = int(np.clip(4 * current_volume, 0, 4))

        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 10
                if self.randomcolor:
                    self.colorlist = []
                    for i in range(8):
                        color = hsv_to_rgb(uniform(0, 1), 1, 1)
                        self.colorlist.append(color)

            if self.counter > 0:
                self.counter -= 1
                runtime_size = int(self.counter/2)


        if self.channel == 'Trigger' and self.randomcolor:
            for i in range(3):
                world[i,0:runtime_size,0:runtime_size,0:runtime_size] = self.colorlist[0][i]
                world[i,0:runtime_size,0:runtime_size,10-runtime_size:] = self.colorlist[1][i]
                world[i,0:runtime_size,10-runtime_size:,0:runtime_size] = self.colorlist[2][i]
                world[i,10-runtime_size:,0:runtime_size,0:runtime_size] = self.colorlist[3][i]
                world[i,0:runtime_size,10-runtime_size:,10-runtime_size:] = self.colorlist[4][i]
                world[i,10-runtime_size:,0:runtime_size,10-runtime_size:] = self.colorlist[5][i]
                world[i,10-runtime_size:,10-runtime_size:,0:runtime_size] = self.colorlist[6][i]
                world[i,10-runtime_size:,10-runtime_size:,10-runtime_size:] = self.colorlist[7][i]

        else:
            # switch on corners
            world[:,0:runtime_size,0:runtime_size,0:runtime_size] = 1.0
            world[:,0:runtime_size,0:runtime_size,10-runtime_size:] = 1.0
            world[:,0:runtime_size,10-runtime_size:,0:runtime_size] = 1.0
            world[:,10-runtime_size:,0:runtime_size,0:runtime_size] = 1.0
            world[:,0:runtime_size,10-runtime_size:,10-runtime_size:] = 1.0
            world[:,10-runtime_size:,0:runtime_size,10-runtime_size:] = 1.0
            world[:,10-runtime_size:,10-runtime_size:,0:runtime_size] = 1.0
            world[:,10-runtime_size:,10-runtime_size:,10-runtime_size:] = 1.0


        return np.clip(world, 0, 1)
