import numpy as np

class s_strobo:

    def __init__(self):
        self.counter = 10
        self.lastworld = np.zeros([3, 10, 10, 10])

    def __call__(self, world):

        if self.counter > 0:
            if self.counter % 2 == 0:
                world[:, :, :, :] = 0.0

            self.counter -= 1

        return world, self.counter
