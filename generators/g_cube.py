# modules
from itertools import cycle
from multiprocessing import shared_memory
import numpy as np

class g_cube():
    '''
    Generator: cube
    a cube in the cube
    Parameters:
    - size
    - sides y/n : just the edges or also the sides of the cube?
    - s2l channel
    '''

    def __init__(self):
        # parameters
        self.size = 4
        self.sides = False

        self.amount = 1.0
        self.channel = 4

        self.sizes = cycle([0,1,2,3,4])

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastvalue = 0
        self.counter = 0

    #Strings for GUI
    def return_values(self):
        return [b'cube', b'size', b'surface', b'channel', b'']

    def return_gui_values(self):
        if self.sides == False:
            sides = 'Off'
        else:
            sides = 'On'

        if 4 > self.channel >= 0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.size,2)), sides, channel, ''),'utf-8')


    def __call__(self, args):
        self.size = round(args[0]*4)
        if args[1] < 0.5:
            self.sides = False
        else:
            self.sides = True
        self.channel = int(args[2]*5)-1

        # create world
        world = np.zeros([3, 10, 10, 10])
        # create smaller world
        tempworld = np.zeros([10, 10, 10])

        if not self.sides:
            tempworld[:, :, :] = -1.0

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))

            # apply threshold
            if current_volume > 0:
                size = next(self.sizes)
            else:
                size = 0

        #check for trigger
        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0

            if self.counter < 6:
                size = next(self.sizes)
                self.counter += 1
            else:
                size = 0

        else:
            size = self.size

        # write cube
        # x slices
        tempworld[4-size, 4-size:6+size, 4-size:6+size] += 1
        tempworld[5+size, 4-size:6+size, 4-size:6+size] += 1
        # y slices
        tempworld[4-size:6+size, 4-size, 4-size:6+size] += 1
        tempworld[4-size:6+size, 5+size, 4-size:6+size] += 1
        # z slices
        tempworld[4-size:6+size, 4-size:6+size, 4-size] += 1
        tempworld[4-size:6+size, 4-size:6+size, 5+size] += 1

        # path world together
        world[0, :, :, :] = tempworld
        world[1, :, :, :] = tempworld
        world[2, :, :, :] = tempworld

        return np.clip(world, 0, 1)
