# modules
import numpy as np
from random import randint, choice
from multiprocessing import shared_memory

class g_circles_revis():
    '''
    Generator: kreise halt
    '''

    def __init__(self):
        self.number = 1
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.soundsize = 1
        self.lastvalue = 0
        self.counter = 0
        self.channel = 0
        self.counter_total = 0
        self.mode = 'out'
        self.speed = 1
        self.z = 4
        self.pause = 4

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

        self.sizes = {}
        self.sizes[2] = self.size2
        self.sizes[3] = self.size3
        self.sizes[4] = self.size4
        self.sizes[5] = self.size5

    #Strings for GUI
    def return_values(self):
        return [b'circles revis', b'mode', b'speed', b'pause', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(self.mode, str(self.speed), str(self.pause), channel),'utf-8')


    def __call__(self, args):

        if args[0] < 0.5:
            self.mode = 'out'

        self.speed = int(args[1]*5) + 1
        self.pause = int(args[2]*10)

        world = np.zeros([3, 10, 10, 10])

        if self.mode == 'out':

            # waiting time
            if 3 < self.counter < self.pause + 3:
                # self.counter = -1
                # self.z = choice([4,5])
                world[0, :, :, np.clip(self.z,0,9)] = self.sizes[5]

            # get bigger
            elif self.counter <= 3:
                self.z = self.z + choice([0,1,-1])
                world[0, :, :, np.clip(self.z,0,9)] = self.sizes[self.counter+2]

            elif self.counter > self.pause + 3:
                self.z = choice([4,5])
                self.counter = -1

        world[0, :, :, :] = np.rot90(world[0, :, :, :], k = 2)
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]


        self.counter_total += 1
        if self.counter_total % self.speed == 0:
            self.counter += 1

        if self.counter == -1:
            self.counter = 0

        return np.clip(world, 0, 1)
