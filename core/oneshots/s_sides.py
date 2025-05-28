import numpy as np

class s_sides:

    def __init__(self):
        self.counter = 6

    def __call__(self, world):
        if self.counter == 6:
            world[:, :, :, 0] = 1.0
            self.counter -= 1
        elif self.counter == 5:
            world[:, 0, :, :] = 1.0
            self.counter -= 1
        elif self.counter == 4:
            world[:, :, 9, :] = 1.0
            self.counter -= 1
        elif self.counter == 3:
            world[:, :, 0, :] = 1.0
            self.counter -= 1
        elif self.counter == 2:
            world[:, 9, :, :] = 1.0
            self.counter -= 1
        elif self.counter == 1:
            world[:, :, :, 9] = 1.0
            self.counter -= 1

        return world, self.counter
