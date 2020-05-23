# modules
import numpy as np
from generators.g_cube import g_cube
from itertools import cycle

class g_multicube():


    def __init__(self):
        self.counter = 0

	    # counter for changes
        self.strobo_frames = 4

        # initialize generator
        self.generator = g_cube()

        self.sizes = cycle([1/4, 2/4, 3/4, 4/4])
        self.size = next(self.sizes)

    #Strings for GUI
    def return_values(self):
        return [b'g_multicubes', b'', b'', b'', b'']

    def __call__(self, args):
        # create world
        world = np.zeros([3, 10, 10, 10])

        if self.counter % 2 == 0:
            world = self.generator([self.size, 0, 0, 0])

        if self.strobo_frames <= 0:
            self.strobo_frames = 4
            self.size = next(self.sizes)
        else:
            self.strobo_frames -= 1

        self.counter += 1

        return np.clip(world, 0, 1)
