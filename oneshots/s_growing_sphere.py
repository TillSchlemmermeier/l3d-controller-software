import numpy as np
from generators.g_genhsphere import gen_hsphere
from colorsys import rgb_to_hsv, hsv_to_rgb
from random import uniform


class s_growing_sphere:

    def __init__(self):
        self.counter = 8
        color = uniform(0, 1)
        self.color = hsv_to_rgb(color, 1, 1)

    def __call__(self, world):

        if self.counter > 0:
            newworld = gen_hsphere(8-self.counter, 4.5, 4.5, 4.5)

            for i in range(3):
                world[i, :, :, :] += newworld[:, :, :]
                world[i, :, :, :] *= self.color[i]

            self.counter -= 1

        return world, self.counter
