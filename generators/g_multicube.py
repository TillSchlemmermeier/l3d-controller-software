# modules
import numpy as np
from generators.g_cube import g_cube
from itertools import cycle
from multiprocessing import shared_memory

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
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0


    #Strings for GUI
    def return_values(self):
        return [b'g_multicubes', b'speed', b'strobo', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.strobo_frames,2)), str(round(self.strobo,2)), '', channel),'utf-8')


    def __call__(self, args):
        # create world
        world = np.zeros([3, 10, 10, 10])
        self.strobo_frames = 10-int(args[0]*10)
        self.strobo = int(round(args[1]+1))
        self.channel = int(args[3]*4)-1

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                world = self.generator([self.size, 0, 0, 0])
            self.size = next(self.sizes)


        elif self.counter % self.strobo == 0:
            world = self.generator([self.size, 0, 0, 0])

            if self.strobo_frame <= 0:
                self.strobo_frame = self.strobo_frames
                self.size = next(self.sizes)
            else:
                self.strobo_frame -= 1

        self.counter += 1

        return np.clip(world, 0, 1)
