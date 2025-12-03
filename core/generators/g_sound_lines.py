# modules
import struct
import numpy as np
from random import randint, uniform
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory


class g_sound_lines():
    '''
    Generator: sound_lines

    Generate random vertical lines when triggered by sound

    Parameters:
    - wait time
    - random color for each square on / Off
    - Pause duration between new squares
    - s2l channel, channel 4 = Trigger mode
    '''

    def __init__(self):

        self.number = 10
        # get initial random lines
        self.lines = []
        for i in range(self.number):
            self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])

        self.counter = 1
        self.reset = 20
        self.randomcolor = False
        self.spectrum = 0
        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastvalue = 0
        self.channel = 0

    def return_state(self):
        return [
            ['number', 'number', round(self.number,2)],
            ['Wait', 'reset', round(self.reset,2)],
            ['Color', 'randomcolor', 'On' if self.randomcolor else 'Off'],
            ['Channel', 'channel', self.channel],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.number = int(args[0]*15)
        self.reset = args[1]*20+1
        self.randomcolor = args[2] > 0.5
        self.channel = [0, 1, 2, 3, 'Trigger'][int(args[3]*4)]
        # === PARAMETERS END ===

        # now we can world with the sound
        world = np.zeros([3, 10, 10, 10])

        if self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.spectrum = uniform(0,1)
                self.lines = []
                for i in range(self.number):
                    self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])

                # get lines
                for line in self.lines:
                    world[:, line[0], line[1], line[2]] = current_volume

                    if self.randomcolor:
                        low = np.clip(self.spectrum - 0.08, 0, 1)
                        high = np.clip(self.spectrum + 0.08, 0, 1)
                        color = hsv_to_rgb(uniform(low, high), 1, 1)
                        for i in range(3):
                            world[i, :, :, :] *= color[i]


        else:
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]

            # get lines
            for line in self.lines:
                world[:, line[0], line[1], line[2]] = current_volume

                if self.randomcolor:
                    low = np.clip(self.spectrum - 0.08, 0, 1)
                    high = np.clip(self.spectrum + 0.08, 0, 1)
                    color = hsv_to_rgb(uniform(low, high), 1, 1)
                    for i in range(3):
                        world[i, :, :, :] *= color[i]

            if self.counter > self.reset:
                self.spectrum = uniform(0,1)
                self.lines = []
                # reset lines
                for i in range(self.number):
                    self.lines.append([slice(0, 10, 1), randint(0, 9), randint(0, 9)])

                self.counter = 0

            self.counter += 1


        return np.round(np.clip(world, 0, 1), 3)
