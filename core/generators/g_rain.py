# modules
import struct
import numpy as np
from random import randint
from multiprocessing import shared_memory

class g_rain():
    '''
    Generator: rain
    '''

    def __init__(self):
        self.numbers = 1
        self.fade = 0.5
        self.lastworld = np.zeros([10, 10, 10])
        self.direction = 'down'
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 'noS2L'
        self.lastvalue = 0
        self.counter = 0

    def return_state(self):
        return [
            ['number', 'numbers', round(self.numbers,2)],
            ['fade', 'fade', round(self.fade,2)],
            ['direction', 'direction', self.direction],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.numbers = int(args[0]*10 + 1)
        self.fade = args[1]
        self.direction = ['down', 'up'][round(args[2])]
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[3]*5)]
        # === PARAMETERS END ===

        # create world
        world = np.zeros([3, 10, 10, 10])

        # move last world 1 step down
        if self.direction == 'down':
            self.lastworld = np.roll(self.lastworld, axis = 0, shift=1)
            self.lastworld[ 0, :, :] = 0.0

            # check if S2L is activated
            if isinstance(self.channel, int):
                current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
                self.numbers = int(10 * current_volume)
                for i in range(self.numbers):
                    world[0,0,randint(0, 9),randint(0, 9)] = 1.0

            #check for trigger
            elif self.channel == 'Trigger':
                current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
                if current_volume > self.lastvalue:
                    self.lastvalue = current_volume
                    self.counter = 5
                if self.counter >= 0:
                    self.numbers = self.counter
                    self.counter -= 1
                    for i in range(self.numbers):
                        world[0,0,randint(0, 9),randint(0, 9)] = 1.0

            # turn on random leds in upper level
            else:
                for i in range(self.numbers):
                    world[0,0,randint(0, 9),randint(0, 9)] = 1.0

        else:
            self.lastworld = np.roll(self.lastworld, axis = 0, shift=-1)
            self.lastworld[ 9, :, :] = 0.0

            # check if S2L is activated
            if isinstance(self.channel, int):
                current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
                self.numbers = int(10 * current_volume)
                # turn on random leds in lower level
                for i in range(self.numbers):
                    world[0,9,randint(0, 9),randint(0, 9)] = 1.0

            #check for trigger
            elif self.channel == 'Trigger':
                current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
                if current_volume > self.lastvalue:
                    self.lastvalue = current_volume
                    self.counter = 5
                if self.counter >= 0:
                    self.numbers = self.counter
                    self.counter -= 1
                    # turn on random leds in lower level
                    for _ in range(self.numbers):
                        world[0,9,randint(0, 9),randint(0, 9)] = 1.0

            # turn on random leds in lower level
            else:
                for _ in range(self.numbers):
                    world[0,9,randint(0, 9),randint(0, 9)] = 1.0

        # add last frame
        world[0,:,:,:] += self.lastworld *self.fade
        self.lastworld[:,:,:] = world[0,:,:,:]

        # copy to other colors
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        return np.clip(world, 0, 1)
