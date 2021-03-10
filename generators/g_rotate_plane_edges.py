# modules
import numpy as np
from scipy.ndimage.interpolation import rotate
from scipy.spatial.transform import Rotation as R
from multiprocessing import shared_memory
from random import randint

class g_rotate_plane():
    def __init__(self):
        self.original = np.zeros([10,10,10])
        for i in range(8):
            self.original[8:9, 1:-1, 1:-1] = 1
            self.edge_list = [[0, 0, 1], #  0
                              [0, 9, 1], #  1
                              [9, 0, 1], #  2
                              [9, 9, 1], #  3
                              [0, 1, 0], #  4
                              [0, 1, 9], #  5
                              [9, 1, 0], #  6
                              [9, 1, 9], #  7
                              [1, 0, 0], #  8
                              [1, 0, 9], #  9
                              [1, 9, 0], # 10
                              [1, 9, 9]] # 11
    #Strings for GUI
    def return_values(self):
        return [b'rotate_plane', b'', b'', b'', b'']


    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format('', '', '', ''),'utf-8')

    #def generate(self, step, dumpworld):
    def __call__(self, args):

        # create world
        world = np.zeros([3, 10, 10, 10])


        # rotate
        newworld = rotate(self.original, self.real_xspeed,
                          axes = (1,2), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.real_yspeed,
                          axes = (0,1), order = 1,
	                      mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.real_zspeed,
                          axes = (0,2), order = 1,
	                      mode = 'nearest', reshape = False)

        # insert array
        world[0, :, :, :] = newworld
        world[1, :, :, :] = newworld
        world[2, :, :, :] = newworld



        return np.clip(world, 0, 1)
