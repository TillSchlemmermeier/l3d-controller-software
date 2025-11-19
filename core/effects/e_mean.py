import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import fftconvolve
from multiprocessing import shared_memory

class e_mean():
    '''Effect: blur with optional s2l'''

    def __init__(self):
        self.amount = 0.1
        self.direction = 'uniform'
        self.channel = 0.0
        self.sound_values = shared_memory.SharedMemory(name="global_s2l_memory")
        self.kernel_uniform = np.ones([3, 3, 3]) / 26.0

    def return_state(self):
        return [
            ['amount', 'amount', round(self.amount, 1)],
            ['direction', 'direction', self.direction],
            ['channel', 'channel', self.channel],
        ]

    def gaussian_2d(self, width):
      x, y = np.meshgrid(np.linspace(-1, 1, 10), np.linspace(-1, 1, 10))
      d = np.sqrt(x*x + y*y)
      sigma = width + 0.0001
      return np.exp(-(d**2 / (2.0 * sigma**2)))

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount = args[0]
        self.direction = ['uniform', 'vertical', 'up', 'down'][int(args[1]*3)]
        self.channel = ['Off', 0, 1, 2, 3][int(args[2]*4)]
        # === PARAMETERS END ===

        if isinstance(self.channel, int):
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8], 'utf-8'))
            sigma = self.amount * current_volume
        else:
            sigma = self.amount

        if self.direction == 'uniform':
            if isinstance(self.channel, int):
                # Sound mode: 2D Gaussian per layer
                gaussian = self.gaussian_2d(sigma)
                for i in range(3):
                    for j in range(10):
                        blurred = fftconvolve(world[i, j, :, :], gaussian, mode='same')
                        world[i, j, :, :] = (1 - self.amount) * world[i, j, :, :] + self.amount * blurred
            else:
                # Normal mode: 3D kernel
                for i in range(3):
                    blurred = fftconvolve(world[i, :, :, :], self.kernel_uniform, mode='same')
                    world[i, :, :, :] = (1 - self.amount) * world[i, :, :, :] + self.amount * blurred

        elif self.direction == 'vertical':
            for i in range(3):
                world[i] = gaussian_filter(world[i], sigma=[sigma, 0, 0], mode='wrap')

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


