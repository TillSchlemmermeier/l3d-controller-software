# modules
import numpy as np
from generators.test import gen_torus

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


    #Strings for GUI
    def return_values(self):
        return [b'torus', b'radius', b'thickness', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.radius,2)), str(round(self.thickness,2)), '', ''),'utf-8')

    #def control(self, maxsize, growspeed, oscillate):
    def __call__(self, args):
        self.radius     = args[0]*10
        self.thickness  = args[1]*3

        #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

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
