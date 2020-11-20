# modules
import numpy as np
from random import randint
from generators.g_sphere_f import gen_sphere
from multiprocessing import shared_memory

class g_soundball():

    def __init__(self):
        self.pos = [4.5, 4.5, 4.5]
        self.speed = [0.0, 0.0, 0.0]
        self.size = 3
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.dt = 0.1
        self.mass = 1.0
        self.spring = 1.0

    def return_values(self):
        return [b'sphere', b'size', b'mass', b'spring', b'dt']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.size,2)),
                                                               str(round(self.size,2)),
                                                               str(round(self.size,2)),
                                                               str(round(self.size,2))),'utf-8')


    def __call__(self, args):
        self.size = round(args[0]*10)
        self.mass = args[1] * 10
        self.spring = args[2] * 10
        self.dt = np.round(args[3], 1)

        world = np.zeros([3, 10, 10, 10])

        # first, generate sphere
        world[0,:,:,:] = gen_sphere(self.size, self.pos[0], self.pos[1], self.pos[2])
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        # update coordinates
        for i in range(3):
            sound_force = float(str(self.sound_values.buf[i*8:i*8+8],'utf-8'))

            # F_ges = -kx + soundforce
            force = - self.spring * np.sqrt((self.pos[i]-4.5)**2)
                       + sound_force

            # v = a*t = F/m * t
            self.speed[i] += force/self.mass * self.dt

            # s = s_0 + v*t
            self.pos[i] += self.speed[i] * self.dt

        return np.clip(world, 0, 1)
