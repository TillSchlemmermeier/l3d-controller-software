# modules
import numpy as np
from matplotlib import colormaps
from scipy.signal import sawtooth

class e_colormaps():
    '''
    '''

    def __init__(self):

        self.mode   = 'space'
        self.map    = 'virids'
        self.speed  = 0.1
        self.length = 1.0

        self.direction = 1

        self.counter = 0

        gradients = ['viridis', 'plasma', 'inferno', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdBu', 'RdYlBu', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'hsv', 'gist_earth', 'terrain', 'gnuplot', 'gnuplot2', 'CMRmap', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral']
        self.gradient_lists = {}
        for gradient in gradients:
            self.gradient_lists[gradient] = colormaps.get(gradient)

    def return_state(self):
        return [
            ['Mode', 'mode', self.mode],
            ['Map', 'map', self.map],
            ['Speed', 'speed', round(self.speed,2)],
            ['Length', 'length', round(self.length,2)],
        ]
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.mode = 'space'
        self.map = list(self.gradient_lists.keys())[round(args[1]*len(self.gradient_lists)-1)]
        self.speed  = args[2]
        self.length = args[3]*4
        # === PARAMETERS END ===

        if self.mode == 'space':
            first_value = sawtooth(self.counter, width = 0.5)*0.5 + 0.5
            last_value  = sawtooth(self.counter + self.length, width = 0.5)*0.5 + 0.5
            color_list  = self.gradient_lists[self.map](np.linspace(first_value,
                                                                    last_value,
                                                                    10))


            # choose color according to x position
            for x in range(10):
                for i in range(3):
                    world[i,x,:,:] = world[i,x,:,:] * color_list[x, i]


        self.counter += self.direction * self.speed


        return np.clip(world, 0, 1)
