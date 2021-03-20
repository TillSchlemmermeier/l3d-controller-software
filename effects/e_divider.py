# modules
import numpy as np
from colorsys import hsv_to_rgb
from random import random
from multiprocessing import shared_memory

class e_divider():
    def __init__(self):
        self.colors = []
        for i in range(8):
            self.colors.append(hsv_to_rgb(random(), 1, 1))

        self.blocks = []
        self.blocks.append([slice(0, 5), slice(0, 5), slice(0, 5)])
        self.blocks.append([slice(5, 10), slice(0, 5), slice(0, 5)])
        self.blocks.append([slice(5, 10), slice(5, 10), slice(0, 5)])
        self.blocks.append([slice(5, 10), slice(5, 10), slice(5, 10)])
        self.blocks.append([slice(0, 5), slice(5, 10), slice(5, 10)])
        self.blocks.append([slice(0, 5), slice(0, 5), slice(5, 10)])
        self.blocks.append([slice(0, 5), slice(5, 10), slice(0, 5)])
        self.blocks.append([slice(5, 10), slice(0, 5), slice(5, 10)])
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.trigger = 0
        self.lastvalue = 0

    def return_values(self):
        return [b'divider', b'', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format('', '', '',''),'utf-8')

    def __call__(self, world, args):
        current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
        if current_volume > self.lastvalue:
            self.lastvalue = current_volume
            self.colors = []
            for i in range(8):
                self.colors.append(hsv_to_rgb(random(), 1, 1))

        for block, color in zip(self.blocks,self.colors):
            for i in range(3):
                world[i, block[0], block[1], block[2]] *= color[i]

        return world
