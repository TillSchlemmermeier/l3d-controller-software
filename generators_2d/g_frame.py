# modules
import numpy as np

class g_frame():
    def __init__(self, resolution):
        self.resolution = resolution

    def return_values(self):
        return [b'frame', b'', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format('', '', '', ''),'utf-8')

    def __call__(self, args):
        world = np.zeros([3, self.resolution[0], self.resolution[1]])
        world[:, 0, :]  = 1.0
        world[:, -1, :] = 1.0
        world[:, :, 0]  = 1.0
        world[:, :, -1] = 1.0
        return world
