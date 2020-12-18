# modules
import numpy as np
from random import randint
from generators.g_sphere_f import gen_sphere
from multiprocessing import shared_memory

class g_soundball():

    def __init__(self):
        self.pos = [0, 4.5, 4.5]
        self.speed = [0.0, 0.0, 0.0]
        self.size = 3
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.dt = 0.01
        self.mass = 10.0
        self.spring = 10000.0

    def return_values(self):
        return [b'sphere', b'size', b'mass', b'spring', b'dt']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.size,2)),
                                                               str(round(self.mass,2)),
                                                               str(round(self.spring,2)),
                                                               str(round(self.dt,2))),'utf-8')


    def __call__(self, args):
        self.size = round(args[0]*10)
        self.mass = args[1] * 20 + 0.1
        self.spring = args[2] * 10000 + 1000
        self.dt = 0.01*args[3]+0.01

        world = np.zeros([3, 10, 10, 10])

        # first, generate sphere
        world[0,:,:,:] = gen_sphere(self.size, self.pos[0], self.pos[1], self.pos[2])
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        # update coordinates
        for i in range(3):
            sound_force = float(str(self.sound_values.buf[i*8:i*8+8],'utf-8'))

            # F_ges = -kx + soundforce
            force = - self.spring * (self.pos[i]-4.5) + 0.1*sound_force

            # v = v_0 + a*t - v*b = v_0 + F/m * t - v*b
            self.speed[i] = round(self.speed[i] + force/self.mass * self.dt - self.speed[i]*0.5,3)

            # s = s_0 + v*t
            self.pos[i] = round(self.pos[i] + self.speed[i] * self.dt,3)

        return np.clip(world, 0, 1)
