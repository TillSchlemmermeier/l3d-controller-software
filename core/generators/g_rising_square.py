# modules
import numpy as np
from random import randint, uniform
from colorsys import hsv_to_rgb
from multiprocessing import shared_memory

class g_rising_square():
    '''
    Generator: rising_square

    a square going from bottom to top

    Parameters:
    - speed
    - random color for each square on / Off
    - Pause duration between new squares
    - s2l channel, channel 4 = Trigger mode
    '''

    def __init__(self):
        self.nled = 1
        self.speed = 2
        self.pause = 2
        self.random = 0
        self.flatworld = np.zeros([3, 4,10,10])
        self.step = 0
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.counter = 0

    def return_state(self):
        return [
            ['speed', 'speed', round(7-self.speed,2)],
            ['color', 'random', 'On' if self.random else 'Off'],
            ['pause', 'pause', round(self.pause,2)],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.speed = 7-int((args[0]*6))
        self.random = args[1] > 0.5
        self.pause = int(round((args[2]+0.06)*30)+1)
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][round(args[3]*5)]
        # === PARAMETERS END ===

        world = np.zeros([3,10,10,10])

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                if not self.random:
                    for i in range(self.nled):
                        self.flatworld[:, :, 9, :] = 1.0

                else:
                    for i in range(self.nled):
                        color = hsv_to_rgb(uniform(0, 1), 1, 1)

                        self.flatworld[0, :, 9, :] = color[0]
                        self.flatworld[1, :, 9, :] = color[1]
                        self.flatworld[2, :, 9, :] = color[2]

        #check if s2l trigger is activated
        elif self.channel == 'Trigger':
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0

            if self.counter < 6 and self.counter % 2 == 0:
                if not self.random:
                    for i in range(self.nled):
                        self.flatworld[:, :, 9, :] = 1.0

                else:
                    for i in range(self.nled):
                        color = hsv_to_rgb(uniform(0, 1), 1, 1)
                        for i in range(3):
                            self.flatworld[i, :, 9, :] = color[i]

                self.counter += 1


        elif self.step % self.pause == 0:
            if not self.random:
                for i in range(self.nled):
                    self.flatworld[:, :, 9, :] = 1.0

            else:
                for i in range(self.nled):
                    color = hsv_to_rgb(uniform(0, 1), 1, 1)

                    self.flatworld[0, :, 9, :] = color[0]
                    self.flatworld[1, :, 9, :] = color[1]
                    self.flatworld[2, :, 9, :] = color[2]

        world[:, :, :, 0] = self.flatworld[:, 0, :, :]
        world[:, :, 9, :] = self.flatworld[:, 1, :, :]
        world[:, :, :, 9] = self.flatworld[:, 2, :, :]
        world[:, :, 0, :] = self.flatworld[:, 3, :, :]



        if self.step % self.speed == 0:
            self.flatworld = np.roll(self.flatworld, shift = -1, axis = 2)
            self.flatworld[:, :, 9, :] = 0.0

        self.step += 1

        return np.clip(world, 0, 1)
