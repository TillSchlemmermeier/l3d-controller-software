# modules
import numpy as np
from colorsys import hsv_to_rgb
from random import random

class e_divider():
    def __init__(self):
        self.blocks = []
        self.block.append([slice(0, 5), slice(0, 5), slice(0, 5)])
        self.block.append([slice(5, 10), slice(0, 5), slice(0, 5)])
        self.block.append([slice(5, 10), slice(5, 10), slice(0, 5)])
        self.block.append([slice(5, 10), slice(5, 10), slice(5, 10)])
        self.block.append([slice(0, 5), slice(5, 10), slice(5, 10)])
        self.block.append([slice(0, 5), slice(0, 5), slice(5, 10)])
        self.block.append([slice(0, 5), slice(5, 10), slice(0, 5)])
        self.block.append([slice(5, 10), slice(0, 5), slice(5, 10)])

    def return_values(self):
        return [b'divider', b'', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format('', '', '', ''),'utf-8')

    def __call__(self, world, args):


        for block in blocks:
            color = hsv_to_rgb(random(), 1, 1)
            for i in range(3):

                world[i, *block] *= color[i]

        return world
