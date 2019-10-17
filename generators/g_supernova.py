import numpy as np
from random import uniform
from generators.g_supernova_f import gen_supernova

class g_supernova():

    def __init__(self):
        self.refresh = 16   # number of frames after creating a new shooting star
        self.speed = 1.0    # moving speed
        self.vectors = []
        self.number = 2
        for i in range(self.number):
            a, b = gen_line(self.speed)
            self.vectors.append([a,b])

    def control(self, refresh, speed, number):
        self.refresh = int(round(refresh*20)+1)
        self.speed = 0.5*(speed+0.1)
        self.number = int(number*10)+1

    def label(self):
        return ['refresh',round(self.refresh,2),'speed', round(self.speed,2),'empty','empty']

    def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # every <refresh> frames: generate new vector
        if step == 1 or step % self.refresh == 0:
            self.vectors = []
            for i in range(self.number):
                a, b = gen_line(self.speed)
                self.vectors.append([a,b])

        for vector in self.vectors:
            [sx, sy, sz] = s(vector[0], vector[1], step % self.refresh)
            # print(sx, sy, sz)
            world[0,:,:,:] += gen_supernova(sx,sy,sz)

        # return current position of shooting star

        # switch on leds depending on distance
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        return np.clip(world, 0, 1)

def gen_line(speed):
    # generate outside point
    # adjust angles for falling down shooting stars!
    p2 = polar2z(10, uniform(0, np.pi), uniform(-np.pi, np.pi))

    # generate a point somewhere in the middle
    p1 = [4.5, 4.5, 4.5]

    v = []
    # calculate vector
    v.append(speed*(p2[0]))
    v.append(speed*(p2[1]))
    v.append(speed*(p2[2]))

    return p1, v

def s(s0, v, t):
    # cartesian coordinates of a point on the line
    x = s0[0] + v[0]*t
    y = s0[1] + v[1]*t
    z = s0[2] + v[2]*t
    return np.round([x, y, z], 2)

def polar2z(r, theta, phi):
    # polar coordinates to cartesian
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return np.round([x, y, z],2)
