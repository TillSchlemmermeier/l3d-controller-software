# modules
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
from multiprocessing import shared_memory
from matplotlib import colormaps
from itertools import cycle
from scipy.signal import sawtooth

class e_colormaps():
    '''
    '''

    def __init__(self):

        # self.c1 = 0.1
        # self.c2 = 0.4
        # self.old_c1 = 0.1
        # self.old_c2 = 0.4

        self.mode   = 'space'
        self.map    = 'virids'
        self.speed  = 0.1
        self.length = 1.0

        self.direction = 1

        self.counter = 0

        # self.balance = 1.0
        # self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        gradients = ['viridis', 'plasma', 'inferno', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdBu', 'RdYlBu', 'Spectral', 'coolwarm', 'bwr', 'managua', 'twilight', 'hsv', 'gist_earth', 'terrain', 'gnuplot', 'gnuplot2', 'CMRmap', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral']
        self.gradient_lists = {}
        for gradient in gradients:
            self.gradient_lists[gradient] = colormaps.get(gradient)
        # self.gradient_lists['viridis'] = colormaps.get('viridis')
        # self.gradient_lists['plasma'] = colormaps.get('plasma')
        # self.gradient_lists['jet'] = colormaps.get('jet')

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
            '''
            color_list = self.gradient_lists[self.map](np.linspace(self.counter%5,
                                                                   np.clip(self.counter%5 + self.length,0,1),
                                                                   5))
            color_list = np.append(color_list, color_list[::-1, :], axis = 0)
            print(color_list[:, 0])
            '''
            first_value = sawtooth(self.counter, width = 0.5)*0.5 + 0.5
            last_value  = sawtooth(self.counter + self.length, width = 0.5)*0.5 + 0.5
            color_list  = self.gradient_lists[self.map](np.linspace(first_value,
                                                                    last_value,
                                                                    10))


            # color_list = cycle(color_list)

            # choose color according to x position
            for x in range(10):
                for i in range(3):
                    world[i,x,:,:] = world[i,x,:,:] * color_list[x, i]


        self.counter += self.direction * self.speed


        return np.clip(world, 0, 1)
