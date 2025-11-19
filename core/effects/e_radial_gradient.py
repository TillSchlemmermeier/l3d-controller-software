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
        self.balance = 6.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4
        self.counter = 0

        self.mode = 'full'
        self.speed = 10

        self.old_c1 = [0.0,0.0,0.0]
        self.old_c2 = [0.0,0.4,0.0]
        # distance to the center for each voxel
        self.distances = {}
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    self.distances[x*100+10*y+z] = np.round(np.sqrt((x-4.5)**2+(y-4.5)**2+(z-4.5)**2),2)

    def return_state(self):
        return [
            ['Color In', 'c1', round(self.c1[0],1)],
            ['ColorOut', 'c2', round(self.c2[0],1)],
            ['mode', 'mode', self.mode],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.c1[0] = args[0]
        self.c2[0] = args[1]
        self.mode = ['full', 'dual', 'fixed'][round(args[2]*2)]
        self.channel = ['noS2L', 0, 1, 2, 3][round(args[3]*4)]
        # === PARAMETERS END ===

        runtime_c1 = self.c1
        runtime_c2 = self.c2

        # check if s2l is activated
        if isinstance(self.channel, int) and self.mode == 'full':
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))

            dif = np.abs(runtime_c1[0] - runtime_c2[0])

            runtime_c1[0] = self.old_c1[0] + current_volume / 40
            runtime_c1[0] = runtime_c1[0] % 1
            runtime_c2[0] = self.old_c2[0] + (current_volume + dif) / 40
            runtime_c2[0] = runtime_c2[0] % 1
            self.old_c1[0] = runtime_c1[0]
            self.old_c2[0] = runtime_c2[0]

        elif self.mode == 'dual':
#            print(self.counter, self.c1[0], self.c2[0], end = '')
            temp = runtime_c1[0]
            runtime_c1[0] = runtime_c1[0] + (runtime_c2[0]-runtime_c1[0])*(np.sin(self.counter/self.speed)+1)*0.5
            runtime_c2[0] = temp + (runtime_c2[0]-temp)*(np.sin(self.counter/self.speed + np.pi)+1)*0.5
#            print('->', np.sin(self.counter/self.speed), self.c1[0], self.c2[0])

        for lamp in list(self.distances.keys()):
            dist = self.distances[lamp]
            # 0 -> -1
            # 8.6 -> 1
            color = hsv_to_rgb(self.sigmoid(2*dist/8.2-1.25)*(runtime_c1[0]-runtime_c2[0])+runtime_c2[0], 1, 1)
            x = int(lamp/100)
            y = int((lamp-x*100)/10)
            z = int(lamp-x*100-y*10)

            world[0, x, y, z] *= color[0]
            world[1, x, y, z] *= color[1]
            world[2, x, y, z] *= color[2]

        if self.mode != 'fixed':
            self.counter += 1

        return np.clip(world, 0, 1)


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x*self.balance))
