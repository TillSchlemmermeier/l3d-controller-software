# modules
import numpy as np
from random import randint
from multiprocessing import shared_memory


class g_randomlines():

    def __init__(self):
        self.reset = 1
        self.counter = 0
        self.saveworld = np.zeros([3,10,10,10])

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.counter = 0
        self.linelist = []

    def return_values(self):
        return [b'randomlines', b'wait', b'', b'', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = 'Trigger'
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.reset,2)), '', '', channel),'utf-8')

    def __call__(self, args):
        self.reset = int(args[0]*10)+1
        self.channel = int(args[3]*5)-1

        world = np.zeros([3, 10, 10, 10])

        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                direction = randint(0, 2)
                if direction == 0:
                    world[:, :, randint(0, 9), randint(0, 9)] = 1

                elif direction == 1:
                    world[:, randint(0, 9), :, randint(0, 9)] = 1
                elif direction == 2:
                    world[:, randint(0, 9), randint(0, 9), :] = 1

        elif self.channel == 4:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0

                for in range(8):
                    direction = randint(0, 2)
                    a = randint(0, 9)
                    b = randint(0, 9)
                    if direction == 0:
                        world[:, :, a, b] = 1
                    elif direction == 1:
                        world[:, a, :, b] = 1
                    elif direction == 2:
                        world[:, a, b, :] = 1

                    self.linelist.append(direction)
                    self.linelist.append(a)
                    self.linelist.append(b)

                    i += 1

                if self.counter < 8:
                    direction = self.linelist[3*self.counter]
                    a = self.linelist[3*self.counter + 1]
                    b = self.linelist[3*self.counter + 2]
                    if direction == 0:
                        world[:, :, a, b] = 0
                    elif direction == 1:
                        world[:, a, :, b] = 0
                    elif direction == 2:
                        world[:, a, b, :] = 0

                    self.counter += 1


        elif self.counter % self.reset == 0:
            direction = randint(0, 2)
            if direction == 0:
                world[:, :, randint(0, 9), randint(0, 9)] = 1
            elif direction == 1:
                world[:, randint(0, 9), :, randint(0, 9)] = 1
            elif direction == 2:
                world[:, randint(0, 9), randint(0, 9), :] = 1

        else:
            world = self.saveworld

        self.counter += 1

        self.saveworld = world
        return np.clip(world, 0, 1)
