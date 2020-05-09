# modules
import numpy as np
from scipy.ndimage import zoom

class e_zoom():
    '''Effect: zoom'''

    def __init__(self):
        self.amount = 0.5
        self.degree = 1

    #strings for GUI
    def return_values(self):
        return [b'zoom', b'amount', b'degree', b'', b'']

    def __call__(self, world, args):
		# parse input
        self.amount = args[0]
        self.degree = int(args[1]*3+1)

        zoomworld = np.zeros([3, 10, 10, 10])

        for i in range(self.degree):
            for c in range(3):
                zoomworld[c, :, :, :] += zoom(world[c, :, :; :], i, mode = 'constant')[5:-5, 5:-5, 5:-5]

        return np.clip(world+self.amount*zoomworld, 0, 1)
