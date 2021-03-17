# modules
import numpy as np
from random import choice, uniform
from generators.g_genhsphere import gen_hsphere
from colorsys import rgb_to_hsv, hsv_to_rgb


class a_multi_cube_edges():
    '''
    Automat: pulsating
    '''

    def __init__(self):#
        self.counter = 0
        self.wait_frames = 50

        # initialize generator
        self.corner_list = [[   0, 8, 4], # A
                            [-0.1, 5, 9], # B
                            [   6, 2,-8], # C
                            [  -9,-2, 7], # D
                            [   1,10,-4], # E
                            [11, -5, -1], # F
                            [ 3, -6,-10], # G
                            [-11,-3, -7]] # H

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

    #Strings for GUI
    def return_values(self):
        return [b'a_multi_cube_edges', b'wait', b'speed', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.wait_frames,2)), str(round(self.speed,2)), '', ''),'utf-8')


    def __call__(self, args):
        self.wait_frames = int(args[0] * 100)+5
        self.speed = args[1]

        # create world
        world = np.zeros([3, 10, 10, 10])

        # choose new corner
        if self.counter > self.wait_frames:
            self.counter = 0

        elif self.counter <= 19:
            # create gaussian profile
            row = np.linspace(0, 19, 20)
            row = np.exp(-np.abs(row - self.counter))**2

            for corner in self.corner_list:
                # first edge
                edge1 = self.edge_list[int(abs(corner[0]))]
                if corner[0] >= 0:
                    world[0, edge1[0], edge1[1], edge1[2]] += row[5:15]
                else:
                    world[0, edge1[0], edge1[1], edge1[2]] += row[5:15][::-1]

                edge2 = self.edge_list[int(abs(corner[1]))]
                if corner[1] >= 0:
                    world[0, edge2[0], edge2[1], edge2[2]] += row[5:15]
                else:
                    world[0, edge2[0], edge2[1], edge2[2]] += row[5:15][::-1]

                edge3 = self.edge_list[int(abs(corner[2]))]
                if corner[2] >= 0:
                    world[0, edge3[0], edge3[1], edge3[2]] += row[5:15]
                else:
                    world[0, edge3[0], edge3[1], edge3[2]] += row[5:15][::-1]

            self.counter += self.speed

        else:
            self.counter += 1
        # copy world together
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        return np.clip(world, 0, 1)
