import numpy as np
from multiprocessing import shared_memory

class g_square_equalizer():

    def __init__(self):
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

        self.amount = [0.5,0.5,0.5,0.5]
        self.pos = [5,5,5,5]

    def return_state(self):
        return [
            ['amount 1', 'amount[0]', round(self.amount[0],2)],
            ['amount 2', 'amount[1]', round(self.amount[1],2)],
            ['amount 3', 'amount[2]', round(self.amount[2],2)],
            ['amount 4', 'amount[3]', round(self.amount[3],2)],
        ]

    def __call__(self, args):
        # get arguments
        for i in range(4):
            self.amount[i] = args[i]*15

        world = np.zeros([3, 10, 10, 10])

        # draw box
        for i in range(4):
            current_volume = float(str(self.sound_values.buf[i*8:i*8+8],'utf-8'))
            current_volume = np.clip(int(current_volume*self.amount[i]),0,9)
            if current_volume > self.pos[i]:
                self.pos[i] = current_volume
            else:
                self.pos[i] -= 1

            self.pos[i] = np.clip(self.pos[i], 0, 9)

            world[:, self.pos[i], i:10-i, i] = 1.0
            world[:, self.pos[i], i:10-i, 9-i] = 1.0
            world[:, self.pos[i], i, i:10-i] = 1.0
            world[:, self.pos[i], 9-i, i:10-i] = 1.0

        return world
