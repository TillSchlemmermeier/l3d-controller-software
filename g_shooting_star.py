import numpy as np
from random import uniform


class g_shooting_star():
    '''
    Generator: shooting star

    a shooting star from somewhere through the cube

    '''

    def __init__(self):
        self.refresh = 16   # number of frames after creating a new shooting star
        self.speed = 1.0    # moving speed
        self.s0, self.v = gen_line(self.speed)

    def control(self, refresh, speed, blub1):
        self.refresh = int(round(refresh*20)+1)
        self.speed = 0.5*(speed+0.1)

    def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # every <refresh> frames: generate new vector
        if step == 1 or step % self.refresh == 0:
            self.s0, self.v = gen_line(self.speed)

        [sx, sy, sz] = s(self.s0, self.v, step % self.refresh)
        # return current position of shooting star
        '''
        try:
            [sx, sy, sz] = s(s0, v, step % self.refresh)
        except:
            s0, v = gen_line(1)
            [sx, sy, sz] = s(s0, v, step % self.refresh)
        '''
        #print(sx,sy,sz)
        # switch on leds depending on distance
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    world[:, x, y, z] = 1.0/((np.sqrt((sx-x)**2 + \
                                                      (sy-y)**2 + \
                                                      (sz-z)**2)))**8

        return world

def gen_line(speed):
    # generate outside point
    # adjust angles for falling down shooting stars!
    #p1 = polar2z(10, uniform(-2, 2), uniform(0, np.pi))
    p1 = [uniform(-1, 10),uniform(-1, 10),  -1]

    # generate a point somewhere in the middle
    p2 = [uniform(1, 8),uniform(1, 8),  10]

    v = []
    # calculate vector
    v.append(speed*(p2[0] - p1[0]))
    v.append(speed*(p2[1] - p1[1]))
    v.append(speed*(p2[2] - p1[2]))

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
