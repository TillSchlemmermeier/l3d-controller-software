# modules
import numpy as np
from scipy.stats import multivariate_normal

# fortran routine is in g_sphere_f.f90

class g_gauss():

    def __init__(self):
        self.sigma = 0

    def control(self, sigma, blub, blub0):
        self.sigma = round(sigma*1.2)

    def label(self):
        return ['sigma',round(self.sigma,2),'empty', 'empty','empty','empty']

    def generate(self, step, dumpworld):

        world = np.zeros([3, 10, 10, 10])

        x, y = np.mgrid[0:10:10j, 0:10:10j]

        # Need an (N, 2) array of (x, y) pairs.
        xy = np.column_stack([x.flat, y.flat])

        mu = np.array([4.5, 4.5])

        sigma = np.array([1.2, 1.2])
        covariance = np.diag(sigma**2)


        for x in range (10)
            for y in range (10)
                for z in range (10)
                    gauss = multivariate_normal.pdf(xy, mean=mu, cov=covariance)*100+5
                    # Reshape back to a (10, 10) grid.
                    gauss = gauss.reshape(x.shape)
                    world[:,x,y,z] = 1.0/(z-gauss)**8

        return np.clip(world, 0, 1)
