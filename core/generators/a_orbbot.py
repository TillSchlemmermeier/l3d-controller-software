# modules
import numpy as np
from generators.g_orbiter import g_orbiter

class a_orbbot():
    '''
    Generator: Testbot
    '''

    def __init__(self):
        self.counter = 1
        self.generator = g_orbiter()
        self.radspeed = 0.01
        self.turnspeed = 0.0
    #Strings for GUI
    def return_values(self):
        return [b'a_orbbot', b'rad_speed', b'turnspeed', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.radspeed,2)), str(round(self.turnspeed,2)), '', ''),'utf-8')


    def __call__(self, args):
        self.radspeed = args[0] * 0.01
        self.turnspeed = args[1]-0.5
        # create world
        world = np.zeros([3, 10, 10, 10])


        world[:, :, :, :] = self.generator([0.5*(np.sin(self.counter * self.radspeed)*0.5+0.5), 0.65+self.turnspeed*2, 0.05+self.turnspeed, 0])

        self.counter += 1

        return np.clip(world, 0, 1)
