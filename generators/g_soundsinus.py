# modules
import numpy as np
from multiprocessing import shared_memory

class g_soundsinus():
    '''
    Generator: soundsinus
    '''
    def __init__(self):

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.speed = 0.1
        self.amps = np.zeros(4)
        self.base_amp = 0.2

    def return_values(self):
        return [b'g_soundsinus', b'speed', b'', b'', b'']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.speed,2)), '', '', ''),'utf-8')


    def __call__(self, args):
        self.speed = args[0]
        world = np.zeros([3, 10, 10, 10])

        # get amplitudes
        for i in range(4):
            self.amps[i] = float(str(self.sound_values.buf[i*8:i*8+8],'utf-8'))

        x = np.linspace(0, 11, 12)
        pos = self.amps[0]*np.sin(np.pi*x/11) #  + self.amps[1]*np.sin(2*np.pi*x/11)
        pos = np.round((4 * pos) , 0).astype(int)
        pos = np.clip(pos, 0, 9)
        for z in range(10):
            world[:, pos[z+1], 4:6, z] = 1.0

        return world
