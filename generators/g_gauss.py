# modules
import numpy as np
from scipy.stats import multivariate_normal
from multiprocessing import shared_memory
#from generators.gen_gauss import gen_gauss

# fortran routine is in g_sphere_f.f90

class g_gauss():

    def __init__(self):
        self.sigma = 1
        self.amplitude = 30
        self.speed = 1
        self.step = 0

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

    #Strings for GUI
    def return_values(self):
        return [b'gauss', b'sigma', b'amplitude', b'speed', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.sigma,2)), str(round(self.amplitude,2)), str(round(self.speed,2)), channel),'utf-8')


    def __call__(self, args):
        self.sigma = args[0]*5+1
        self.amplitude = args[1]*50
        self.speed = args[2]
        self.channel = int(args[3]*4)-1


        world = np.zeros([3, 10, 10, 10])

        y, z = np.mgrid[0:10:10j, 0:10:10j]

        # Need an (N, 2) array of (x, y) pairs.
        yz = np.column_stack([y.flat, z.flat])

        mu = np.array([5, 5])

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            sigma = np.array([5*current_volume+1,5*current_volume+1])

        else:
            sigma = np.array([self.sigma,self.sigma])

        covariance = np.diag(sigma**2)

        gauss = np.sin(self.step*self.speed)*multivariate_normal.pdf(yz, mean=mu, cov=covariance)*self.amplitude*self.sigma**2+5
        gauss = gauss.reshape(10,10)
        self.step += 1
        world[0,:,:,:] = gen_gauss(gauss)

        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

#        for y in range (10):
#            for z in range (10):
#                for x in range (10):
#                    world[:,x,y,z] = np.exp(-abs(x-gauss[y,z])*5)

        return np.clip(world, 0, 1)
