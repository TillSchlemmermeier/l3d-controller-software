# modules
import numpy as np


class g_pyramid():
    '''
    Generator: pyramid
    '''

    def __init__(self):
        self.rotspeed = 0.1
        self.ps = []
        self.ps.append(4.5,  0)
        self.ps.append(4.5, 90)
        self.ps.append(4.5,180)
        self.ps.append(4.5,270)

    def control(self, rotspeed):
        self.rotspeed = rotspeed

    def label(self):
        return ['rotation speed',round(self.rotspeed, 2),'empty', 'empty'','empty','empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        points = []
        for p in self.ps:
            points.append(polar2z(p))

        for p in points:
            line = gen_line(p)
            world1 = np.ones([10, 10, 10])

            # calculate distance of all points
            for x in range(10):
                for y in range(10):
                    for z in range(10):
                        dist1 = (np.cross(p-[x,y,z],line)
                        world1[x,y,z] = 1.0/dist1**8

            world[0,:,:,:] += world

        # create next step
        self.p1[1] += self.rotspeed
        self.p2[1] += self.rotspeed
        self.p3[1] += self.rotspeed
        self.p4[1] += self.rotspeed

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    dist1 = (self.p1)

        return np.clip(world, 0, 1)


def gen_line(p1,p2 = (9,4.5,4.5)):

    v = []
    # calculate vector
    v.append(temp[0] - p1[0])
    v.append(temp[1] - p1[1])
    v.append(temp[2] - p1[2])

    return v

def polar2z(r, theta):
    # polar coordinates to cartesian
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    return [0, x, y]

def s(s0, v, t):
    # cartesian coordinates of a point on the line
    x = s0[0] + v[0]*t
    y = s0[1] + v[1]*t
    z = s0[2] + v[2]*t
    return [x, y, z]
