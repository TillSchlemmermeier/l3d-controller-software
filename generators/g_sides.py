# modules
import numpy as np
from random import randint
from multiprocessing import shared_memory

class g_sides():
    '''
    Generator: sides
    One side of a cube is on

    Parameters:
    size of cube
    Sound2Light channel
    '''

    def __init__(self):
        self.size = 4
        self.sides = True
        self.side = 0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    #Strings for GUI
    def return_values(self):
        return [b'cube', b'size', b'', b'', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.size,2)), '', '', channel),'utf-8')


    def __call__(self, args):
        self.size = round(args[0]*4)
        self.channel = int(args[3]*5)-1

        # create world
        world = np.zeros([3, 10, 10, 10])
        # create smaller world
        tempworld = np.zeros([10, 10, 10])


        if not self.sides:
            tempworld[:, :, :] = -1.0

        size = self.size

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                # select side
                self.side = randint(0, 5)

        #check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                # select side
                self.side = randint(0, 5)

        else:
            # select side
            self.side = randint(0, 5)

        if self.side == 0:
            tempworld[4-size, 4-size:6+size, 4-size:6+size] += 1
        elif self.side == 1:
            tempworld[5+size, 4-size:6+size, 4-size:6+size] += 1
        elif self.side == 2:
            tempworld[4-size:6+size, 4-size, 4-size:6+size] += 1
        elif self.side == 3:
            tempworld[4-size:6+size, 5+size, 4-size:6+size] += 1
        elif self.side == 4:
            tempworld[4-size:6+size, 4-size:6+size, 4-size] += 1
        elif self.side == 5:
            tempworld[4-size:6+size, 4-size:6+size, 5+size] += 1

        # path world together
        world[0, :, :, :] = tempworld
        world[1, :, :, :] = tempworld
        world[2, :, :, :] = tempworld

        return np.clip(world, 0, 1)
