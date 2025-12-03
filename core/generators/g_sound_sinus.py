# modules
import struct
import numpy as np
from multiprocessing import shared_memory

class g_sound_sinus():
    '''
    Generator: soundsinus
    '''
    def __init__(self):

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.speed = 0.1
        self.amps = np.zeros(4)
        self.base_amp = 0.2

    def return_state(self):
        return [
            ['speed', 'speed', round(self.speed,2)],
        ]

    def __call__(self, args):
        # === PARAMETERS START ===
        self.speed = args[0]
        # === PARAMETERS END ===

        world = np.zeros([3, 10, 10, 10])

        # get amplitudes
        for i in range(4):
            self.amps[i] = struct.unpack('d', bytes(self.sound_values.buf[i*8:i*8+8]))[0]

        x = np.linspace(0, 11, 12)
        pos = self.amps[0]*np.sin(np.pi*x/11) #  + self.amps[1]*np.sin(2*np.pi*x/11)
        pos = np.round((4 * pos) , 0).astype(int)
        pos = np.clip(pos, 0, 9)
        for z in range(10):
            world[:, pos[z+1], 4:6, z] = 1.0

        return world
