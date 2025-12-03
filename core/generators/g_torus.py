# modules
import struct
import numpy as np
from .g_torus_f import gen_torus
from multiprocessing import shared_memory

class g_torus():
    '''
    Generator: torus

    creates a torus

    Parameters:
    - radius
    - thickness
    '''

    def __init__(self):
        self.radius = 6
        self.thickness = 3
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.counter = 0
        self.lastvalue = 0

    def return_state(self):
        return [
            ['radius', 'radius', round(self.radius,2)],
            ['thickness', 'thickness', round(self.thickness,2)],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.radius = args[0]*8
        self.thickness = args[1]*3
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[2]*5)]
        # === PARAMETERS END ===

        #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            if current_volume > 0:
                self.radius = current_volume * self.radius
            else:
                self.radius = 0

        elif self.channel == 'Trigger':
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0
            if self.counter < 9:
                self.radius = 8 - self.counter
                self.counter += 1
            else:
                self.radius = 0

        # create torus
        n = 25
        theta = np.linspace(0, 2.*np.pi, n)
        px = (self.radius * np.cos(theta))
        py = [4.5 for x in range(n)]
        pz = (self.radius * np.sin(theta))

        world[0, :, :, :] = gen_torus(n, self.thickness, px, py, pz)
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
        return np.clip(world, 0, 1)
