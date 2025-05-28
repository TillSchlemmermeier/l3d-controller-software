import numpy as np
#from generators.g_genhsphere import gen_hsphere
#from generators.g_gensphere import gen_sphere#
from generators.g_genssphere import gen_sphere

#gen_central_glow
#! compile with f2py3 -c -m gen_sphere g_growing_sphere_solid.f90

class s_dark_sphere:

    def __init__(self):
        self.n_frames = 25
        self.counter = self.n_frames
#        self.substract_world = np.zeros([10, 10, 10])

    def __call__(self, world):

        if self.counter > 0:
#            self.substract_world  = np.clip(self.substract_world + 1.5*gen_sphere(10-self.counter, 4.5, 4.5, 4.5),0,2)
            world = np.clip(world, 0, 1)

            if self.counter > self.n_frames/2:
                tempworld = gen_sphere(self.n_frames-self.counter, 4.5, 4.5, 4.5)
                for i in range(3):
                    world[i, :, :, :] -= tempworld[:, :, :]

            else:
                tempworld = gen_sphere(self.n_frames-self.counter*2, 4.5, 4.5, 4.5)
                tempworld -= 1
                for i in range(3):
                    world[i, :, :, :] += tempworld[:, :, :]

            self.counter -= 0.6

        return np.clip(world, 0, 1), self.counter
