# modules
import numpy as np
from scipy.ndimage import zoom

class e_zoom():
    '''Effect: zoom'''

    def __init__(self):
        self.amount = 0.5
        self.degree = 2

    #strings for GUI
    def return_values(self):
        return [b'zoom', b'amount', b'degree', b'', b'']

    def __call__(self, world, args):
		# parse input
        self.amount = args[0]
        self.degree = int(args[1]*3+1)

        zoomworld = np.zeros([3, 10, 10, 10])

#        print(np.shape(world[0, :, :, :]))
#        print(np.shape(zoomworld[0, :, :, :]))
#        print(np.shape(zoom(world[0, :, :, :], 2, mode = 'constant')))
#        print(np.shape(zoom(world[0, :, :, :], 2, mode = 'constant')[5:-5, 5:-5, 5:-5]))

        for c in range(3):
            world[c, :, :, :] = zoom(world[c, :, :, :], 2, mode = 'constant')[5:-5, 5:-5, 5:-5]

        return np.clip(world+self.amount*zoomworld, 0, 1)
