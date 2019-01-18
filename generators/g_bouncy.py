import numpy as np
from random import uniform
from generators.g_shooting_star_f import gen_shooting_star

class g_bouncy():
    '''
    Generator: shooting star

    a shooting star from somewhere through the cube
    '''

    def __init__(self):
        self.speed = 10    # moving speed

        # first points
        self.p1 = [10, uniform(-1, 10),uniform(-1, 10)]
        self.p2 = [-1, uniform(-1, 10),uniform(-1, 10)]

        self.switch = 1
        self.p = self.p1

        self.direction = 0
        self.v = gen_line(self.p1, self.p2, self.speed)

    def control(self, speed, blub0, blub1):
        self.speed = int((speed*20)+5)
        self.direction = int(round(blub0*2+0.5))

    def label(self):
        return ['speed', round(self.speed,2),'direction',self.direction, 'empty', 'empty']

    def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # every <refresh> frames: generate new vector
        if step == 0 or step % self.speed == 0:
            self.switch *= -1
            if self.switch == -1:

                self.v = gen_line(self.p1, self.p2, self.speed)
                self.p = self.p1
                self.p1 = [10, uniform(-1, 10),uniform(-1, 10)]
            else:
                self.v = gen_line(self.p2, self.p1, self.speed)
                self.p = self.p2
                self.p2 = [-1, uniform(-1, 10),uniform(-1, 10)]

        [sx, sy, sz] = s(self.p, self.v, step % self.speed)

        # switch on leds depending on distance
        world[0,:,:,:] = np.rot90(gen_shooting_star(sx,sy,sz), axes = [0,1], k=0)

        if self.direction == 1:
            world[0, :, :, :] = np.rot90(world[0, :, :, :], k = 1, axes = (0,1))
        elif self.direction == 2:
            world[0, :, :, :] = np.rot90(world[0, :, :, :], k = 1, axes = (0,2))

        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]
        return np.clip(world, 0, 1)

def gen_line(p1, p2, speed):

    v = []
    # calculate vector
    v.append(p2[0] - p1[0])
    v.append(p2[1] - p1[1])
    v.append(p2[2] - p1[2])

    # normalize
    length = np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)*0.1/speed
    #print(np.array(v)*length)
    return np.array(v)*length

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
