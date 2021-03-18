import numpy as np
from multiprocessing import shared_memory
from colorsys import hsv_to_rgb
from random import uniform

class g_square_equalizer():

    def __init__(self):
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0
        self.lastvalue = 0
        self.colorlist =[]

        self.amount = [0.5,0.5,0.5,0.5]
        self.pos = [5,5,5,5]

    def return_values(self):
        return [b'square_equalizer', b'amount 1', b'amount 2', b'amount 3', b'amount 4']

    def return_gui_values(self):

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount[0],2)),
                                                               str(round(self.amount[1],2)),
                                                               str(round(self.amount[2],2)),
                                                               str(round(self.amount[3],2))),'utf-8')

    def __call__(self, args):
        # get arguments
        for i in range(4):
            self.amount[i] = args[i]*15

        world = np.zeros([3, 10, 10, 10])
        trigger = int(float(str(self.sound_values.buf[32:40],'utf-8')))
        if trigger > self.lastvalue:
            self.lastvalue = trigger
            self.counter = 10
            self.colorlist = []
            for i in range(4):
                color = hsv_to_rgb(uniform(0, 1), 1, 1)
                self.colorlist.append(color)

        # draw box
        for i in range(4):
            current_volume = float(str(self.sound_values.buf[i*8:i*8+8],'utf-8'))
            current_volume = np.clip(int(current_volume*self.amount[i]),0,9)
            print(current_volume)
            if current_volume > self.pos[i]:
                self.pos[i] = current_volume
            else:
                self.pos[i] -= 1

            self.pos[i] = np.clip(self.pos[i], 0, 9)


            for j in range(3):
                world[j, self.pos[i], i:10-i, i] = self.colorlist[i][j]
                world[j, self.pos[i], i:10-i, 9-i] = self.colorlist[i][j]
                world[j, self.pos[i], i, i:10-i] = self.colorlist[i][j]
                world[j, self.pos[i], 9-i, i:10-i] = self.colorlist[i][j]

        return world
