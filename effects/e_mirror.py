# modules
import numpy as np

class e_mirror():

    def __init__(self):
        self.naxis = 1

    def return_values(self):
        return [b'naxis', b'', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.naxis), '', '', ''), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.naxis = int(args[0]*2 +1)
        self.fade = args[1]

        tempworld = np.zeros([3, 10, 10, 10])
        tempworld[:, :, :, :] = world[:, :, :, :]

        if self.naxis == 1:
            world[:, :, :, :] += tempworld[:, ::-1, :, :]
        elif self.naxis == 2:
            world[:, :, :, :] += tempworld[:, :, ::-1, :]
            world[:, :, :, :] += tempworld[:, :, :, ::-1]
        elif self.naxis == 3:
            world[:, :, :, :] += tempworld[:, ::-1, :, :]
            world[:, :, :, :] += tempworld[:, :, ::-1, :]
            world[:, :, :, :] += tempworld[:, :, :, ::-1]

        return np.clip(world, 0, 1)
