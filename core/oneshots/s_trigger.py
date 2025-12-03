import numpy as np
from multiprocessing import shared_memory
import struct

class s_trigger:

    def __init__(self):
        self.counter = 1
        self.lastworld = np.zeros([3, 10, 10, 10])
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    def __call__(self, world):

        self.counter = 0
        current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]
        current_volume += 1
        self.sound_values.buf[32:40] = struct.pack('d', current_volume)

        return world, self.counter
