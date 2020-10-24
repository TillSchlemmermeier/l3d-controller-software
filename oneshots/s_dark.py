import numpy as np

class s_dark:

    def __init__(self):
        self.counter = 1
        self.lastworld = np.zeros([3, 10, 10, 10])

    def __call__(self, world):

        if self.counter > 0:
            world *= (1-self.counter)**4
            self.counter -= 0.1

        return world, self.counter
