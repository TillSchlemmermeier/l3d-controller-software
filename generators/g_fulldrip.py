import numpy as np
import scipy
from random import randint
from multiprocessing import shared_memory

class g_fulldrip():

    def __init__(self):
        self.drops = []
        self.n = 20
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

        for i in range(self.n):
            self.drops.append(led())


    def return_values(self):
        return [b'fulldrip', b'number', b'fade in', b'', b'channel']


    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format('', '', '', ''),'utf-8')


    def __call__(self, args):
        self.n = int(args[0]*50)+1

        world = np.zeros([3, 10, 10, 10])

        for i in range(len(self.drops)):
            temp = self.drops[i].run(self.drops)
            if len(temp) == 3:
                world[:, temp[0], temp[1], temp[2]] = 1.0
            else:
                self.drops[i] = led()

        return np.clip(world, 0, 1)**2


class led:
    def __init__(self):
        print('HALLO')
        self.x, self.y, self.z = 0, randint(0,9), randint(0,9)
        self.stop_x = 9# randint(4, 6)
        self.stop_t = randint(10, 40)
        self.state = 'run'


    def run(self, leds):

        # perform action
        if self.state == 'run':
            output = [self.x, self.y, self.z]
            # check for collisions:
            ind = np.where(self.y == np.array([l.x for l in leds]))[0]
            print(ind)
            self.x += 1
        elif self.state == 'wait':
            output = [self.x, self.y, self.z]
            self.stop_t -= 1
        elif self.state == 'dead':
            output = [0]

        # update state
        if self.x > 9 or self.state == 'dead':
            self.state = 'dead'
        else:
            if self.x == self.stop_x and self.state == 'run':
                self.state = 'wait'
            elif self.state == 'wait' and self.stop_t <= 0:
                self.state == 'run'
                self.x += 1

        return np.clip(output,0,9)
