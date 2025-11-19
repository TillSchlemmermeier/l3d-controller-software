import numpy as np
from multiprocessing import shared_memory

class e_fade():
    '''Effect: fade with optional s2l'''

    def __init__(self):
        self.amount = 0.5
        self.channel = 'noS2L'
        self.sound_values = shared_memory.SharedMemory(name="global_s2l_memory")
        self.invert = False
        self.oldworld = np.zeros([3, 10, 10, 10])
        self.counter = 0
        self.countermax = 0

    def return_state(self):
        return [
            ['amount', 'amount', round(self.amount, 1)],
            ['channel', 'channel', self.channel],
            ['invert', 'invert', 'On' if self.invert else 'Off'],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount = args[0]
        self.channel = ['noS2L', 0, 1, 2, 3][round(args[1]*4)]
        self.invert = args[2] > 0.5
        # === PARAMETERS END ===

        # Simple fade if channel is off
        if self.channel == 'noS2L':
            world += self.oldworld * self.amount
            self.oldworld[:, :, :, :] = world[:, :, :, :]
            return np.clip(world, 0, 1)

        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8], 'utf-8'))

        if self.invert:
            # Fade out on sound
            newlength = np.clip(int(7 * current_volume * self.amount), 1, 10)
            if newlength < self.counter:
                self.counter = 0
                self.countermax = newlength

            fade_factor = 0.9 - self.counter / (self.countermax + 0.001)
            self.counter += 1
        else:
            # Fade in on sound
            newlength = int(10 * current_volume * self.amount)
            if newlength > self.counter:
                self.counter = newlength
                self.countermax = self.counter

            fade_factor = self.counter / (self.countermax + 1)
            if self.counter > 0:
                self.counter -= 1

        world += fade_factor * self.oldworld
        self.oldworld[:, :, :, :] = world[:, :, :, :]

        return np.clip(world, 0, 1)