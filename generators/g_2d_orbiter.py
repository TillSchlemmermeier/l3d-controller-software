import numpy as np
from scipy.signal import sawtooth
from generators.sphere2d import sphere2d
from generators.convert2d import convert2d

 
class g_2d_orbiter():
    '''
    Generator: orbiter

    generates a rotating/orbiting object

    Parameters:
    - distance osc/swell
    - angle y swell
    - angle z osc

    '''
    def __init__(self, test = False, dim = [60, 10]):
        self.distance = 2
        self.theta = 0.5
        self.dim = dim
        self.test = test
        self.fade = 4

    def control(self, dist, theta, fade):
        self.distance = dist*8
        self.theta = 3*(theta-0.5)
        self.fade = 3+3*fade

    def label(self):
        return ['distance',round(self.distance,2),'theta', round(self.theta,2),'blub','blub']

    def generate(self, step, dumpworld):
        # generate empty world
        world = np.zeros([3, self.dim[0], self.dim[1]])

        # generate current position
        temp_d = self.distance
        temp_theta = sawtooth(self.theta*step)*np.pi

        [sx, sy] = polar2z(temp_d, temp_theta)

        # switch on leds depending on distance
        world[0,:,:] = sphere2d(sx+self.dim[0]/2-0.5, sy+self.dim[1]/2-0.5, self.fade)
        world[1,:,:] = world[0,:,:]
        world[2,:,:] = world[0,:,:]

        if not self.test:
            # convert it to 2d
            world3d = convert2d(world)
        else:
            world3d = world


        return world3d

def polar2z(r, theta):
    # polar coordinates to cartesian
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return [x, y]
