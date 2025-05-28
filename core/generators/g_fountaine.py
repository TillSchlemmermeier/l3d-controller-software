# modules
import numpy as np
from generators.test import gen_torus
from multiprocessing import shared_memory

class g_fountaine():
    '''
    Generator: torus

    creates a torus

    Parameters:
    - radius
    - thickness
    '''

    def __init__(self):
        self.speed = 1
        self.step = 0
        self.thickness = 1
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.counter = 0
        self.lastvalue = 0
        self.radius = 5
        self.size_change = 0

    def return_state(self):
        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = 'Trigger'
        else:
            channel = 'noS2L'

        return [
            ['speed', 'speed', round(self.speed,2)],
            ['thickness', 'thickness', round(self.thickness,2)],
            ['size change', 'size_change', round(self.size_change,2)],
            ['channel', 'channel', channel],
        ]
    

    def __call__(self, args):
        self.speed     = args[0]*2
        self.thickness  = args[1]*2+0.1
        self.size_change = args[2] # round(args[2]-0.5,1)
        self.channel = int(args[3]*5)-1

        #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                self.radius = current_volume * self.radius
            else:
                self.radius = 0

        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0
            if self.counter < 9:
                self.radius = 8 - self.counter
                self.counter += 1
            else:
                self.radius = 0

        # calculate position
        position = 9 - self.step%10

        # get thickness
        thickness = self.thickness

        # get radius
        radius = np.clip(self.radius*((9-position)/9)**2, 0, 10)

        # create torus
        n = 25
        theta = np.linspace(0, 2.*np.pi, n)
        px = (radius * np.cos(theta))
        py = [position for x in range(n)]
        pz = (radius * np.sin(theta))


        world[0, :, :, :] = np.rot90(gen_torus(n, thickness, px, py, pz), 1, axes = (0,1))
        world[1, :, :, :] = world[0, :, :, :]
        world[2, :, :, :] = world[0, :, :, :]

        '''
        for i in range(n):
            for x in range(10):
                for y in range(10):
                    for z in range(10):
                        dist = np.sqrt((px[i]-x+4.5)**2 + (py[i]-y)**2 + (pz[i]-z+4.5)**2)
                        if dist < self.thickness:
                            world[:,x,y,z] = 1.0
        '''
        self.step += self.speed
        return np.clip(world , 0, 1)
