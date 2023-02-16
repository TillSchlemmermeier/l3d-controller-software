import numpy as np
import multiprocessing as mp
from multiprocessing import shared_memory

class s_trigger:

    def __init__(self):
        self.counter = 1
        self.lastworld = np.zeros([3, 10, 10, 10])
        self.sound_values = mp.shared_memory.SharedMemory(name = "global_s2l_memory")

    def __call__(self, world):

        self.counter = 0

        value = float(str(self.sound_values.buf[32:40],'utf-8'))
        value += 1

        string = '{:8}'.format(value)
        bla = bytearray('{:.8}'.format(string[:8]),'utf-8')
        # increase trigger
        self.sound_values.buf[32:40] = bla

        return world, self.counter
