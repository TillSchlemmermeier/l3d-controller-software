import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb

class s_cubes:

    def __init__(self):
        self.counter = 5
        color = uniform(0, 1)
        self.color = hsv_to_rgb(color, 1, 1)

    def __call__(self, world):

        if self.counter > 0:

            # create smaller world
            tempworld = np.zeros([10, 10, 10])
            tempworld[:, :, :] = -1.0

            size = 5-self.counter

            for i in range(3):
                world[i, :, :, :] = self.counter*world[i, :, :, :] + (1-self.counter)*fftconvolve(world[i, :, :, :], self.mean, mode='same')

            # write cube
            # x slices
            tempworld[4-size, 4-size:6+size, 4-size:6+size] += 1
            tempworld[5+size, 4-size:6+size, 4-size:6+size] += 1
            # y slices
            tempworld[4-size:6+size, 4-size, 4-size:6+size] += 1
            tempworld[4-size:6+size, 5+size, 4-size:6+size] += 1
            # z slices
            tempworld[4-size:6+size, 4-size:6+size, 4-size] += 1
            tempworld[4-size:6+size, 4-size:6+size, 5+size] += 1

            # path world together
            for i in range(3):
                world[i, :, :, :] += tempworld
                world[i, :, :, :] *= self.color[i]

            self.counter -= 1

        return world, self.counter
