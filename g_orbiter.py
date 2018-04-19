import numpy as np
from scipy.signal import sawtooth


class g_orbiter():
    '''
    Generator: orbiter

    generates a rotating/orbiting object

    Parameters:
    - distance osc/swell
    - angle y swell
    - angle z osc

    '''

    def __init__(self):
        self.distance = 4
        self.theta = 0.1
        self.rho = 0.1

    def control(self, dist, theta, rho):
        self.distance = dist
        self.theta = theta
        self.rho = rho

    def generate(self, step, dumpworld):
        # generate empty world
        world = np.zeros([3, 10, 10, 10])

        # generate current position
        temp_d = 3 + np.sin(self.distance*step)
        temp_theta = sawtooth(self.theta*step)
        temp_rho = np.sin(self.rho*step)

        [sx, sy, sz] = polar2z(temp_d, temp_theta, temp_rho)

        # switch on leds depending on distance
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    world[:, x, y, z] = 1.0/((np.sqrt((sx-x)**2 + (sy-y)**2 + (sz-z)**2)))**4

        return world

    def polar2z(r, theta, phi):
        # polar coordinates to cartesian
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return [x, y, z]
