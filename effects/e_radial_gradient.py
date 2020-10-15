# modules
import numpy as np
from colorsys import rgb_to_hsv, hsv_to_rgb
from multiprocessing import shared_memory

class e_radial_gradient():
    '''
    Effect: Radial Gradient

    Parameters:
    - Inner Color
    - Outer Color
    - Balance
    - Sound2Light Channel
    '''

    def __init__(self):

        self.c1 = [0.1,0.0,0.0]
        self.c2 = [0.4,0.4,0.0]
        self.balance = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4

        # distance to the center for each voxel
        self.distances = {}
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    self.distances[x*100+10*y+z] = np.round(np.sqrt((x-4.5)**2+(y-4.5)**2+(z-4.5)**2),2)


    def return_values(self):
        return [b'rad grad', b'Color In', b'ColorOut', b'Balance', b'channel']

    def return_gui_values(self):
        if self.channel < 4:
            channel = str(self.channel)
        elif:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.c1,1)), str(round(self.c2,1)), str(round(self.balance,1)), channel), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.c1[0] = args[0] # hsv_to_rgb(c1,1,1)
        self.c2[0] = args[1] # hsv_to_rgb(c2,1,1)
        self.balance = 4 * args[2] + 0.01
        self.channel = args[3] * 4

        #check if s2l is activated
        if self.channel < 4:
            # apply threshold
            if current_volume > 0:
                self.c1[0] += current_volume / 10
                self.c2[0] += current_volume / 10


        for lamp in list(self.distances.keys()):
            dist = self.distances[lamp]
            # 0 -> -1
            # 8.6 -> 1
            color = hsv_to_rgb(self.sigmoid(2*dist/8.2-1.25)*(self.c1-self.c2)+self.c2, 1, 1)

            x = int(lamp/100)
            y = int((lamp-x*100)/10)
            z = int(lamp-x*100-y*10)

            world[0, x, y, z] *= color[0]
            world[1, x, y, z] *= color[1]
            world[2, x, y, z] *= color[2]

        return np.clip(world, 0, 1)


    def sigmoid(self, x):
        # print(x, 1 / (1 + np.exp(-x*self.balance)))
        return 1 / (1 + np.exp(-x*self.balance))
