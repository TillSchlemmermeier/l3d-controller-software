import numpy as np
import scipy
from random import randint
from multiprocessing import shared_memory

class g_rotating_line:
    def __init__(self):
        self.number = 1
        self.p1 = [randint(2, 7), randint(2, 7), randint(2, 7)]
        self.p2 = [randint(2, 7), randint(2, 7), randint(2, 7)]
        self.wait = 10
        self.counter = 0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    #Strings for GUI
    def return_values(self):
        return [b'rotating_line', b'wait', b'', b'', b'']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.wait,2)), '', '', ''),'utf-8')

    def __call__(self, args):
        self.wait = int(args[0]*20+1)

        world = np.zeros([3, 10, 10, 10])

        world[:, self.p1[0], self.p1[1], self.p1[2]] = 1
        world[:, self.p2[0], self.p2[1], self.p2[2]] = 1

        if self.counter % self.wait == 0:
            self.p1[:] = self.p2[:]
            self.p2 = [randint(2, 7), randint(2, 7), randint(2, 7)]
            self.counter = 0

        self.counter += 1
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    d = get_dist_to_line(self.p1, self.p2, [x,y,z])
                    world[:, x, y, z] = 0.5 * (1/(d+ 0.0001)**8)

#                    if d < 3:
#                        world[0, x, y, z] = 1/(d/3+0.0001)

#        print(np.clip(world, 0, 1))
        return np.round(np.clip(world, 0, 1), 3)


def get_dist_to_line(p1, p2, p3):

    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    return np.linalg.norm(np.cross(p2-p1,p3-p1))/(np.linalg.norm(p2-p1)+0.01)
