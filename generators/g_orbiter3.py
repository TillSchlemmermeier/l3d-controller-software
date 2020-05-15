import numpy as np
from scipy.signal import sawtooth
from generators.g_shooting_star_f import gen_shooting_star

class g_orbiter3():
    '''
    Generator: orbiter

    generates a rotating/orbiting object

    Parameters:
    - distance osc/swell
    - angle y swell
    - angle z osc

    '''
# zentrum falsch
    def __init__(self):
        self.distance = 4
        self.theta = 0.1
        self.rho = 0.1
        self.step = 0

    #Strings for GUI
    def return_values(self):
        return [b'orbiter3', b'distance', b'theta', b'rho', b'']

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.distance = args[0]*8
        self.theta = args[1]
        self.rho = args[2]

        # generate empty world
        world = np.zeros([3, 10, 10, 10])

        # generate current position
        temp_d = self.distance
        temp_theta = sawtooth(self.theta*self.step)*np.pi
        temp_rho = np.sin(self.rho*self.step)

        [sx, sy, sz] = polar2z(temp_d, temp_theta, temp_rho)

        # switch on leds depending on distance
        world[0,:,:,:] = gen_shooting_star(sx+4.5, sy+4.5, sz+4.5)
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        self.step += 1

        return world

def polar2z(r, theta, phi):
    # polar coordinates to cartesian
    y = r * np.sin(theta) * np.cos(phi)
    z = r * np.sin(theta) * np.sin(phi)
    x = r * np.cos(theta)
    return [x, y, z]
