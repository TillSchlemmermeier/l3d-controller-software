# modules
import numpy as np
from scipy.stats import multivariate_normal

# fortran routine is in g_sphere_f.f90

class g_gauss():

    def __init__(self):
        self.sigma = 1
        self.amplitude = 30
        self.speed = 1

    def control(self, sigma, amplitude, speed):
        self.sigma = sigma*5+1
        self.amplitude = amplitude*50
        self.speed = speed

    def label(self):
        return ['sigma',round(self.sigma,2),'amplitude',round(self.amplitude,2), 'speed',round(self.speed,2),'empty','empty']

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])

        y, z = np.mgrid[0:10:10j, 0:10:10j]

        # Need an (N, 2) array of (x, y) pairs.
        yz = np.column_stack([y.flat, z.flat])

        mu = np.array([5, 5])

        sigma = np.array([self.sigma,self.sigma])
        covariance = np.diag(sigma**2)

        gauss = np.sin(step*self.speed)*multivariate_normal.pdf(yz, mean=mu, cov=covariance)*self.amplitude*self.sigma**2+5
        gauss = gauss.reshape(10,10)


        for y in range (10):
            for z in range (10):
                for x in range (10):
                    world[:,x,y,z] = np.exp(-abs(x-gauss[y,z])*5)

        print

        return np.clip(world, 0, 1)
