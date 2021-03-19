# modules
import numpy as np
from random import choice
from multiprocessing import shared_memory

class g_flash():

    def __init__(self):
        self.counter = 0
        self.points = self.gen_line()
        self.reset = 10

        # s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    #Strings for GUI
    def return_values(self):
        return [b'flash', b'', b'', b'', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format('', '', '', channel),'utf-8')


    def __call__(self, args):

        # create world
        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                if self.brightness <=1.0:
                    world[0, self.edge[0], self.edge[1], self.edge[2]] = self.brightness**2
                    self.brightness += current_volume
                else:
                    self.edge = choice(self.edge_list)
                    self.brightness = 0


        if self.counter > self.reset:
            for p in range(self.counter):
                world[0, *self.points[p]] = 1

            self.counter += 1

        else:
            self.counter = 0
            self.points = self.gen_line

        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)

    def gen_line(self):

        points = []
        points.append([0, randint(0,9), [randint(0,9)])

        for i in range(9):
            y = np.clip(points[-1][1] + choice([-1,0,1]), 0, 9)
            z = np.clip(points[-1][2] + choice([-1,0,1]), 0, 9)
            points.append([i, x, y])

        return points
