# modules
import numpy as np
from generators.g_cube import g_cube
from itertools import cycle

class g_multicube():


    def __init__(self):
        self.counter = 0

	    # counter for changes
        self.strobo_frames = 4
        self.strobo_frame = 4
        self.strobo = 2

        # initialize generator
        self.generator = g_cube()

        self.sizes = cycle([0/4, 1/4, 2/4, 3/4, 4/4])
        self.size = next(self.sizes)

    #Strings for GUI
    def return_values(self):
        return [b'g_multicubes', b'speed', b'strobo', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.strobo_frames,2)), str(round(self.strobo,2)), '', ''),'utf-8')


    def __call__(self, args):
        # create world
        world = np.zeros([3, 10, 10, 10])
        self.strobo_frames = 10-int(args[0]*10)
        self.strobo = int(round(args[1]+1))

        if self.counter % self.strobo == 0:
            world = self.generator([self.size, 0, 0, 0])

        if self.strobo_frame <= 0:
            self.strobo_frame = self.strobo_frames
            self.size = next(self.sizes)
        else:
            self.strobo_frame -= 1

        self.counter += 1

        return np.clip(world, 0, 1)
