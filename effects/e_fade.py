# modules
import numpy as np

class e_fade():
    '''Effect: zoom'''

    def __init__(self):
        self.amount = 0.5
        self.oldworld = np.zeros([3, 10, 10, 10])
        self.channel = 0

    # strings for GUI
    def return_values(self):
        return [b'fade', b'amount', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >= 0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,1)), '', '', channel), 'utf-8')


    def __call__(self, world, args):
		# parse input
        self.amount = args[0]

        world += self.oldworld*self.amount
        self.oldworld[:, :, :, :] = world[:, :, :, :]

        return np.clip(world, 0, 1)
