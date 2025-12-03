# modules
import struct
import numpy as np
from multiprocessing import shared_memory

class e_mirror():
    '''
    Effect: e_mirror

    Parameter:
    - Number of axes
    - mode: Axis mirror or point symmetry mirror
    - s2l trigger On / Off
    '''

    def __init__(self):
        self.lastvalue = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.counter = 0
        self.naxis = 1
        self.trigger = 'Off'
        self.steps = 0
        self.mode = 'mirror'

    def return_state(self):
        return [
            ['# of axes', 'naxis', self.naxis],
            ['steps', 'steps', int(self.steps)],
            ['mode', 'mode', self.mode],
            ['s2l trigger', 'trigger', 'On' if self.trigger else 'Off'],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.naxis = int(args[0]*2 +1)
        self.steps = int(args[1]*8)
        self.mode = ['mirror', 'point'][round(args[2])]
        self.trigger = args[3] > 0.5
        # === PARAMETERS END ===

        tempworld = np.zeros([3, 10, 10, 10])
        tempworld[:, :, :, :] = world[:, :, :, :]

        runtime_naxis = self.naxis
        if self.trigger:
            current_volume = struct.unpack('d', bytes(self.sound_values.buf[32:40]))[0]

            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = -1

            self.counter += 1

            if self.counter > self.steps:
                runtime_naxis = 0

        if self.mode == 'mirror':

            if runtime_naxis == 1:
                world[:, :, :, :] += tempworld[:, ::-1, :, :]
            elif runtime_naxis == 2:
                world[:, :, :, :] += tempworld[:, :, ::-1, :]
                world[:, :, :, :] += tempworld[:, :, :, ::-1]
            elif runtime_naxis == 3:
                world[:, :, :, :] += tempworld[:, ::-1, :, :]
                world[:, :, :, :] += tempworld[:, :, ::-1, :]
                world[:, :, :, :] += tempworld[:, :, :, ::-1]
            elif runtime_naxis == 0:
                pass

        else:
            for i in range(3):
                tempworld[i,:,:,:] = np.rot90(tempworld[i,:,:,:], 2, (0, 1))

            for i in range(3):
                tempworld[i,:,:,:] = np.rot90(tempworld[i,:,:,:], 2, (1, 2))

            world[:, :, :, :] += tempworld[:, :, :, :]

        return np.clip(world, 0, 1)
