# modules
import numpy as np
from scipy.stats import multivariate_normal
#from generators.gen_gauss import gen_gauss

# fortran routine is in g_sphere_f.f90

class g_gauss():

    def __init__(self):
        self.sigma = 1
        self.amplitude = 30
        self.speed = 1
        self.step = 0

    #Strings for GUI
    def return_values(self):
        return [b'gauss', b'sigma', b'amplitude', b'speed', b'']

    def __call__(self, args):
        self.sigma = args[0]*5+1
        self.amplitude = args[1]*50
        self.speed = args[2]

        world = np.zeros([3, 10, 10, 10])

        y, z = np.mgrid[0:10:10j, 0:10:10j]

        # Need an (N, 2) array of (x, y) pairs.
        yz = np.column_stack([y.flat, z.flat])

        mu = np.array([5, 5])

        sigma = np.array([self.sigma,self.sigma])
        covariance = np.diag(sigma**2)

        gauss = np.sin(self.step*self.speed)*multivariate_normal.pdf(yz, mean=mu, cov=covariance)*self.amplitude*self.sigma**2+5
        gauss = gauss.reshape(10,10)
        self.step += 1
        #print(gauss)
        world[0,:,:,:] = gen_gauss(gauss)

        #print(world[0,:,0,0])

        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

#        for y in range (10):
#            for z in range (10):
#                for x in range (10):
#                    world[:,x,y,z] = np.exp(-abs(x-gauss[y,z])*5)

        return np.clip(world, 0, 1)
