import numpy as np
import scipy
from random import randint, choice
from multiprocessing import shared_memory
from scipy.ndimage.interpolation import rotate


class g_lightsaber:
    def __init__(self):
        self.speed = 1
        self.fade = 0.2

        self.p_in  = [randint(2, 7), randint(2, 7), randint(2, 7)]
        self.p_out = [randint(2, 7), choice([-3,-2,-1, 10,11,12]), choice([-3,-2,-1, 10,11,12])]
        self.p_top = [-2, self.p_in[0] + randint(-1,1), self.p_in[1] + randint(-1,1)]

        self.wait = 10
        self.counter = 0
        # self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.point = [0,0,0]
        self.old_world = np.zeros([3,10,10,10])

    #Strings for GUI
    def return_values(self):
        return [b'lightsaber', b'wait', b'speed', b'fade', b'']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.wait,2)), str(round(self.speed,2)), str(round(self.fade,2)), ''),'utf-8')

    def __call__(self, args):
        self.wait  = int(args[0]*20+1)
        self.speed = 0.5*args[1]**2+0.0001
        self.fade = args[2]

        world = np.zeros([3, 10, 10, 10])

        #world[:, self.p1[0], self.p1[1], self.p1[2]] = 1
        #world[:, self.p2[0], self.p2[1], self.p2[2]] = 1



        # after waiting time reset
        if self.counter % self.wait == 0 or self.point[2] <= -3:
            self.p_in  = [randint(2, 7), randint(2, 7), randint(2, 7)]

            self.p_out = [choice([-3,-2,-1, 10,11,12]), choice([-3,-2,-1, 10,11,12]), choice([-3,-2,-1, 10,11,12])]
            #self.p_in = [4,4,4]
            self.p_top = [-2, self.p_in[1] + randint(-1,1), self.p_in[2] + randint(-1,1)]
            self.counter = 0
            self.old_world = np.zeros([3,10,10,10])

            #print(self.p_in, self.p_top, self.p_out)

        self.point = get_point(self.p_top, self.p_in, self.counter, self.speed)
        self.counter += 1

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    d = get_dist_to_line(self.p_out, self.point, [x,y,z])
                    world[:, x, y, z] = 0.5 * (1/(d+ 0.0001)**8)

        self.old_world = np.round(np.clip(world, 0, 1), 3) + self.fade * self.old_world

        return np.round(np.clip(self.old_world, 0, 1), 3)


def get_point(p1, p2, step, speed):
    vec = np.array(p2)-np.array(p1)
    p = p1 + step*vec
    return p

def get_dist_to_line(p1, p2, p3):

    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    return np.linalg.norm(np.cross(p2-p1,p3-p1))/(np.linalg.norm(p2-p1)+0.01)
