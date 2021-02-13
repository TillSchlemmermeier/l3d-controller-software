# modules
import numpy as np
from generators.test import gen_torus
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

    #Strings for GUI
    def return_values(self):
        return [b'torus', b'radius', b'thickness', b'', b'channel']

    def return_gui_values(self):
        if 4 > self.channel >=0:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = 'Trigger'
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.radius,2)), str(round(self.thickness,2)), '', channel),'utf-8')

    #def control(self, maxsize, growspeed, oscillate):
    def __call__(self, args):
        self.radius     = args[0]*10
        self.thickness  = args[1]*3
        self.channel = int(args[3]*5)-1

        #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # check if S2L is activated
        if 4 > self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0:
                self.radius = current_volume * 10
            else:
                self.radius = 0

        elif self.channel == 4:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0
            if self.counter < 11:
                self.radius = 10 - self.counter
                self.counter += 1

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
