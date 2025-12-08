# modules
import numpy as np
import struct
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

    def return_state(self):
        return [
            ['speed', 'speed', round(self.speed,2)],
            ['thickness', 'thickness', round(self.thickness,2)],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, args):
        # === PARAMETERS START ===
        self.speed     = args[0]*2
        self.thickness  = args[1]*2+0.1
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][int(args[2]*5)]
        # === PARAMETERS END ===

        #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if isinstance(self.channel, int):
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]
            if current_volume > 0:
                self.radius = current_volume * 5  # Fixed: Use base radius to avoid cumulative scaling
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

        else:  # 'noS2L' mode
            self.radius = 5  # Reset to default fixed radius

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
