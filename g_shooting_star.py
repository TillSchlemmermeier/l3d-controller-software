import numpy as np
from random import uniform


class g_shooting_star():
    '''
    Generator: shooting star

    a shooting star from somewhere through the cube


    '''

    def __init__(self):
        self.refresh = 16
        self.speed = 1.0

    def control(self, refresh, speed, blub1):
        self.refresh = round(refresh*20)
        self.speed = speed

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])

        refresh = 16

        # every <refresh> frames: generate new vector
        if step % refresh == 0:
            s0, v = gen_line(0.8)

        # return current position of shooting star
        try:
            [sx, sy, sz] = s(s0, v, step % refresh)
        except:
            s0, v = gen_line(1)
            [sx, sy, sz] = s(s0, v, step % refresh)

        # switch on leds depending on distance
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    world[:, x, y, z] = 1.0/((np.sqrt((sx-x)**2 + (sy-y)**2 + (sz-z)**2)))**4

        return world

def gen_line(speed):
    # generate two points
    p1 = polar2z(15, uniform(-2, 2), uniform(-2, 2))
    p2 = [uniform(-3, 3), uniform(-3, 3), uniform(-3, 3)]
    v = []
    # calculate vector
    v.append(p2[0] - p1[0])
    v.append(p2[1] - p1[1])
    v.append(p2[2] - p1[2])

    v = speed * v/(np.sqrt(v[0]**2 + v[1]**2 + v[2]**2))
    return p1, v

def s(s0, v, t):
    # cartesian coordinates of a point on the line
    x = s0[0] + v[0]*t
    y = s0[1] + v[1]*t
    z = s0[2] + v[2]*t
    return [x, y, z]

def polar2z(r, theta, phi):
    # polar coordinates to cartesian
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return [x, y, z]
