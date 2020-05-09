# modules
import numpy as np

class e_outer_shadow():
    '''
    Effect: outer_shadow
    '''

    def __init__(self):
        self.radius = 9.0

    #strings for GUI
    def return_values(self):
        return [b'outer_shadow', b'radius', b'', b'', b'']


    def __call__(self, world, args):
        # parsing input
        self.radius = args[0]*10

        posx = 4.5
        posy = 4.5
        posz = 4.5

        for x in range(9):
            for y in range(9):
                for z in range(9):
                    dist = np.sqrt((x-posx)**2+(y-posy)**2+(z-posz)**2)
                    world[:, x, y, z] /= (dist*self.radius)

        return world
