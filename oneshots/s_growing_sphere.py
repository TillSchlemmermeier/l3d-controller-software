import numpy as np
from generators.g_genhsphere import gen_hsphere


class s_growning_sphere:

    def __init__(self):
        self.counter = 8

    def __call__(self, world):

        if self.counter > 0:
            newworld = gen_hsphere(8-self.counter, 4.5, 4.5, 4.5)

            world[0, :, :, :] += newworld[:, :, :]
            world[1, :, :, :] += newworld[:, :, :]
            world[2, :, :, :] += newworld[:, :, :]

            self.counter -= 1

        return world, self.counter
