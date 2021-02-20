# modules
import numpy as np
from random import choice, seed
from multiprocessing import shared_memory


class g_cube_edges():
    '''
    Generator: cube_edges

    selects a random edge and propagates
    a bright spot along the edge.

    '''

    def __init__(self):
        self.counter = 20
        self.speed = 1
        self.number = 1
        # corner_list contains the indices for edges
        # which belong to one corner
        self.corner_list = [[   0, 8, 4], # A
                            [-0.1, 5, 9], # B
                            [   6, 2,-8], # C
                            [  -9,-2, 7], # D
                            [   1,10,-4], # E
                            [11, -5, -1], # F
                            [ 3, -6,-10], # G
                            [-11,-3, -7]] # H
        '''
        E - - F
        |\    |\
        | A - - B
        G | - H |
         \|    \|
          C - - D
        '''

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
                          ]

        self.corner = self.corner_list[0] # choice(self.corner_list)
        self.direction = choice([-1, 1])
        seed()
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0

    #Strings for GUI
    def return_values(self):
        return [b'cube_edges', b'speed', b'number', b'', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), str(round(self.number,2)), '', channel),'utf-8')


    def __call__(self, args):
        self.speed = args[0]*2 + 0.4
        self.number = int(3*args[1])
        if self.number == 0:
            self.number = 1
        self.channel = int(args[3]*5)-1


        # create world
        world = np.zeros([3, 10, 10, 10])

        if self.channel < 4:
            # choose new corner
            if self.counter > 19:
                self.counter = 0
                self.corner = choice(self.corner_list)

        # check if S2L is activated
        elif 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                self.counter = 0
                self.corner = choice(self.corner_list)
                self.speed = 2.4
                self.number = 3

        #check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0
                self.corner = choice(self.corner_list)


        # create gaussian profile
        row = np.linspace(0, 19, 20)
        row = np.exp(-np.abs(row - self.counter))

        # first edge
        edge1 = self.edge_list[int(abs(self.corner[0]))]
        if self.corner[0] >= 0:
            world[0, edge1[0], edge1[1], edge1[2]] = row[5:15]
        else:
            world[0, edge1[0], edge1[1], edge1[2]] = row[5:15][::-1]

        # second edge
        if self.number > 1:
            edge2 = self.edge_list[int(abs(self.corner[1]))]
            if self.corner[1] >= 0:
                world[0, edge2[0], edge2[1], edge2[2]] = row[5:15]
            else:
                world[0, edge2[0], edge2[1], edge2[2]] = row[5:15][::-1]

        if self.number > 2:
            edge3 = self.edge_list[int(abs(self.corner[2]))]
            if self.corner[2] >= 0:
                world[0, edge3[0], edge3[1], edge3[2]] = row[5:15]
            else:
                world[0, edge3[0], edge3[1], edge3[2]] = row[5:15][::-1]

        # increase counter
        self.counter += self.speed

        # brightness : x**3 for linear change
        # see https://de.wikipedia.org/wiki/Stevenssche_Potenzfunktion

        # copy world together
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)
