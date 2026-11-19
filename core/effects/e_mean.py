import struct
import numpy as np
from scipy.ndimage import gaussian_filter, uniform_filter
from multiprocessing import shared_memory

class e_mean():
    '''Effect: blur with optional s2l'''

    def __init__(self):
        self.amount = 0.1
        self.direction = 'uniform'
        self.channel = 0.0
        self.sound_values = shared_memory.SharedMemory(name="global_s2l_memory")

    def return_state(self):
        return [
            ['amount', 'amount', round(self.amount, 1)],
            ['direction', 'direction', self.direction],
            ['channel', 'channel', self.channel],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount = args[0]
        self.direction = ['uniform', 'vertical', 'up', 'down'][int(args[1]*3)]
        self.channel = ['Off', 0, 1, 2, 3][int(args[2]*4)]
        # === PARAMETERS END ===

        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            sigma = self.amount * current_volume
        else:
            sigma = self.amount

        # mode='nearest': a missing neighbour at the edge counts as the edge voxel itself
        if self.direction == 'uniform':
            # the mean of each voxel and its 26 neighbours
            blurred = uniform_filter(world, size=[1, 3, 3, 3], mode='nearest')
            mix = min(sigma, 1)
            world = (1 - mix)*world + mix*blurred

        elif self.direction == 'vertical':
            world = gaussian_filter(world, sigma=[0, sigma, 0, 0], mode='nearest')

        elif self.direction == 'down':
            blend = min(0.5, sigma / 5)
            for i in range(3):
                for z in range(9, 0, -1):
                    world[i, z] = (1 - blend) * world[i, z] + blend * world[i, z-1]

        elif self.direction == 'up':
            blend = min(0.5, sigma / 5)
            for i in range(3):
                for z in range(9):
                    world[i, z] = (1 - blend) * world[i, z] + blend * world[i, z+1]

        return np.clip(world, 0, 1)


