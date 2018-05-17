# modules
import numpy as np

class e_outer_shadow():
    '''
    Effect: outer_shadow
    '''

    def __init__(self):
        self.radius = 9.0

    def control(self, radius, blub0, blub1):
	self.radius = radius*10

    def generate(self, step, world):

        posx = 4.5
        posy = 4.5
        posz = 4.5

        for x in range(9):
            for y in range(9):
                for z in range(9):
                    dist = np.sqrt((x-posx)**2+(y-posy)**2+(z-posz)**2)
                    world[:, x, y, z] /= (dist*self.radius)

        return np.clip(world, 0, 1)
