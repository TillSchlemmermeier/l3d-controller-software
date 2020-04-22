import numpy as np
from random import uniform
from generators.g_shooting_star_f import gen_shooting_star

class g_shooting_star():
    '''
    Generator: shooting star

    a shooting star from somewhere through the cube
    '''

    def __init__(self):
        self.refresh = 16   # number of frames after creating a new shooting star
        self.speed = 1.0    # moving speed
        self.s0, self.v = gen_line(self.speed)
        self.step = 0

    def return_values(self):
        pass

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.refresh = int(round(args[0]*20)+1)
        self.speed = 0.5*(args[1]+0.1)

        world = np.zeros([3, 10, 10, 10])

        # every <refresh> frames: generate new vector
        if self.step == 1 or self.step % self.refresh == 0:
            self.s0, self.v = gen_line(self.speed)

        [sx, sy, sz] = s(self.s0, self.v, self.step % self.refresh)
        # return current position of shooting star
        self.step += 1
        # switch on leds depending on distance
        world[0,:,:,:] = np.rot90(gen_shooting_star(sx,sy,sz), axes = [0,1], k=3)
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]


        return np.clip(world, 0, 1)

def gen_line(speed):
    # generate outside point
    # adjust angles for falling down shooting stars!
    #p1 = polar2z(10, uniform(-2, 2), uniform(0, np.pi))
    p2 = [10, uniform(-1, 10),uniform(-1, 10)]

    # generate a point somewhere in the middle
    p1 = [-1, uniform(4, 5),uniform(4, 5)]

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
