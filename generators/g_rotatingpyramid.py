# modules
import numpy as np


class g_pyramid():
    '''
    Generator: pyramid
    '''

    def __init__(self):
        self.rotspeed = 0.1
        self.brightness = 0.5
        self.ps = []
        self.ps.append([4.5,  0])
        self.ps.append([4.5, 90])
        self.ps.append([4.5,180])
        self.ps.append([4.5,270])

    def control(self, rotspeed, brightness, blub1):
        self.rotspeed = rotspeed
        self.brightness = brightness

    def label(self):
        return ['rotation speed',round(self.rotspeed, 2),'brightness', round(self.brightness, 2),'empty','empty']

    def generate(self, step, dumpworld):
        # create world
        world = np.zeros([3, 10, 10, 10])

        points = []
        for p in self.ps:
            points.append(polar2z(p[0],p[1]))


        for p in points:
            line = gen_line(p)
            world1 = np.ones([10, 10, 10])

            # calculate distance of all points
            for x in range(10):
                for y in range(10):
                    for z in range(10):
                        dist1 = np.linalg.norm(np.cross(np.array(p)-np.array([x,y,z]),line))
                        world1[x,y,z] = np.exp(-dist1*self.brightness)

            world[0,:,:,:] += world1

        # create next step
        for p in self.ps:
            p[1] += self.rotspeed

        return np.clip(world, 0, 1)


def gen_line(p1,p2 = (9,4.5,4.5)):

    v = []
    # calculate vector
    v.append(p1[0] - p2[0])
    v.append(p1[1] - p2[1])
    v.append(p1[2] - p2[2])

    return v

def polar2z(r, theta):
    # polar coordinates to cartesian
    x = r * np.cos(theta/(2*np.pi))
    y = r * np.sin(theta/(2*np.pi))

    return [0, x+4.5, y+4.5]

def s(s0, v, t):
    # cartesian coordinates of a point on the line
    x = s0[0] + v[0]*t
    y = s0[1] + v[1]*t
    z = s0[2] + v[2]*t
    return [x, y, z]
