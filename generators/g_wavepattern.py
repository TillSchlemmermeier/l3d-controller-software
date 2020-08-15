# modules
import numpy as np


class g_wavepattern():
    '''
    Generator: wavepattern
    '''

    def __init__(self):
        self.freq = 0.5
        self.speed = 1.0
        self.step = 0

    #Strings for GUI
    def return_values(self):
        return [b'wavepattern', b'freq', b'speed', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.freq,2)), str(round(self.speed,2)), '', ''),'utf-8')

    #def control(self, freq, speed, blub1):
    def __call__(self, args):
        self.freq = int(args[0]*10)
        self.speed = args[1]*0.5

        world = np.zeros([3, 10, 10, 10])

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    world[:, x, y, z] = np.sin(self.step*self.speed)*(
                                        np.sin(np.pi*self.freq*x/10)**6+\
                                        np.sin(np.pi*self.freq*y/10)**6+\
                                        np.sin(np.pi*self.freq*z/10)**6)
        self.step += 1
        return np.clip(world, 0, 1)
