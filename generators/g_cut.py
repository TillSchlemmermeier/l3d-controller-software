# modules
import numpy as np
from random import choice
from multiprocessing import shared_memory

class g_cut():

    def __init__(self):
        self.speed = 0.1
        self.brightness = 0.0
        self.edge_list = [[0, 0, slice(0, 10)], #  0
                          [0, 9, slice(0, 10)], #  1
                          [9, 0, slice(0, 10)], #  2
                          [9, 9, slice(0, 10)], #  3
                          [0, slice(0, 10), 0], #  4
                          [0, slice(0, 10), 9], #  5
                          [9, slice(0, 10), 0], #  6
                          [9, slice(0, 10), 9], #  7
                          [slice(0, 10), 0, 0], #  8
                          [slice(0, 10), 0, 9], #  9
                          [slice(0, 10), 9, 0], # 10
                          [slice(0, 10), 9, 9], # 11
                          [(0,1,2,3,4,5,6,7,8,9),(0,1,2,3,4,5,6,7,8,9),(0,1,2,3,4,5,6,7,8,9)],
                          [(0,1,2,3,4,5,6,7,8,9),(0,1,2,3,4,5,6,7,8,9),(9,8,7,6,5,4,3,2,1,0)],
                          [(0,1,2,3,4,5,6,7,8,9),(9,8,7,6,5,4,3,2,1,0),(0,1,2,3,4,5,6,7,8,9)],
                          [(9,8,7,6,5,4,3,2,1,0),(0,1,2,3,4,5,6,7,8,9),(0,1,2,3,4,5,6,7,8,9)],
                          [(9,8,7,6,5,4,3,2,1,0),(0,1,2,3,4,5,6,7,8,9),(9,8,7,6,5,4,3,2,1,0)],
                          [(9,8,7,6,5,4,3,2,1,0),(9,8,7,6,5,4,3,2,1,0),(0,1,2,3,4,5,6,7,8,9)],
                          [(9,8,7,6,5,4,3,2,1,0),(9,8,7,6,5,4,3,2,1,0),(9,8,7,6,5,4,3,2,1,0)],
                          ]

        self.edge = choice(self.edge_list)
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0


    #Strings for GUI
    def return_values(self):
        return [b'cut', b'speed', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), '', '', channel),'utf-8')


    def __call__(self, args):
        self.speed = args[0]*0.5 + 0.1
        self.channel = int(args[3]*4)-1

        # create world
        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                if self.brightness <=1.0:
                    self.brightness += current_volume
                else:
                    world[0, self.edge[0], self.edge[1], self.edge[2]] = self.brightness**2
                    self.brightness = 0

        elif self.brightness <= 1.0:
            world[0, self.edge[0], self.edge[1], self.edge[2]] = self.brightness**2
            self.brightness += self.speed

        else:
            self.edge = choice(self.edge_list)
            self.brightness = 0

        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)
