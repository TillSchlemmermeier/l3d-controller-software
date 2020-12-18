# modules
import numpy as np
from random import randint, choice
from multiprocessing import shared_memory


class g_cone():

    def __init__(self):
        self.number = 1
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.soundsize = 1
        self.make_rings = circleworld()
        self.channel = 0
        self.sizes = np.array([0,0,0,0])

    def return_values(self):
        return [b'circles', b'number', b'', b'', b'channel']

    def return_gui_values(self):

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number,2)), '', '', str(self.channel)),'utf-8')


    def __call__(self, args):
        self.number = int(args[0]*10)
        self.channel = int(args[3]*3)


        current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
        current_volume = int(np.clip(3 * current_volume, 0, 3)*3)

        self.sizes = np.roll(self.sizes, 1)
        self.sizes[0] = current_volume
        world = np.zeros([3, 10, 10, 10])

        world[0, :, :] = self.make_rings(*self.sizes)

        # rotate if necessary
        world[0, :, :, :] = np.rot90(world[0, :, :, :], k = 1)
        world[1,:,:,:] = world[0, :, : , :]
        world[2,:,:,:] = world[0, :, : , :]
        return np.clip(world, 0, 1)



class circleworld:

    def __init__(self):
        print('ini circleworld')
        # size 5
        self.size5 = np.zeros([10,10])

        # straight
        self.size5[0,3:7] = 1.0
        self.size5[9,3:7] = 1.0
        self.size5[3:7,0] = 1.0
        self.size5[3:7,9] = 1.0

        # diag
        self.size5[1,2] = 1.0
        self.size5[2,1] = 1.0

        self.size5[1,7] = 1.0
        self.size5[2,8] = 1.0

        self.size5[7,1] = 1.0
        self.size5[8,2] = 1.0

        self.size5[7,8] = 1.0
        self.size5[8,7] = 1.0

        # size 4
        self.size4 = np.zeros([10,10])

        # straight
        self.size4[1,3:7] = 1.0
        self.size4[8,3:7] = 1.0
        self.size4[3:7,1] = 1.0
        self.size4[3:7,8] = 1.0

        # diag
        self.size4[2,2] = 1.0
        self.size4[2,7] = 1.0
        self.size4[7,2] = 1.0
        self.size4[7,7] = 1.0

        # size 3
        self.size3 = np.zeros([10,10])

        # straight
        self.size3[2,3:7] = 1.0
        self.size3[7,3:7] = 1.0
        self.size3[3:7,2] = 1.0
        self.size3[3:7,7] = 1.0

        # size 2
        self.size2 = np.zeros([10,10])

        # straight
        self.size2[3,4:6] = 1.0
        self.size2[6,4:6] = 1.0
        self.size2[4:6,3] = 1.0
        self.size2[4:6,6] = 1.0


    def __call__(self, h1, h2, h3, h4):
        world = np.zeros([10, 10, 10])
        world[:, h1, :] += self.size2[:,:]
        world[:, h2, :] += self.size3[:,:]
        world[:, h3, :] += self.size4[:,:]
        world[:, h4, :] += self.size5[:,:]

        return world
