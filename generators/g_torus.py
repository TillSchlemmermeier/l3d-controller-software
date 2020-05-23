# modules
import numpy as np

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

    #def control(self, maxsize, growspeed, oscillate):
    def __call__(self, args):
        self.radius     = args[0]*10
        self.thickness  = args[1]*5

        #def generate(self, step, dumpworld):
        world = np.zeros([3, 10, 10, 10])

        # create torus
        n = 10
        theta = np.linspace(0, 2.*np.pi, n)
        px = (self.radius * np.cos(theta))
        py = [4.5 for x in range(n)]
        pz = (self.radius * np.sin(theta))

        for i in range(10):
            for x in range(10):
                for y in range(10):
                    for z in range(10):
                        dist = np.sqrt((px[i]-x)**2 + (py[i]-y)**2 + (pz[i]-z)**2)
                        if dist < 1:
                            world[:,x,y,z] = 1.0

        return np.clip(world, 0, 1)
