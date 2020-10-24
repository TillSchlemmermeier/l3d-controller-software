import numpy as np

class s_fade:

    def __init__(self):
        self.counter = 1
        self.lastworld = np.zeros([3, 10, 10, 10])

    def __call__(self, world):

        if self.counter > 0:
            world += self.lastworld*(1-self.counter)
            self.counter -= 0.1

            self.lastworld[:, :, :, :] = world[:, :, :, :]

        return world, self.counter
