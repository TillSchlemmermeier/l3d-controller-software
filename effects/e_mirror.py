# modules
import numpy as np
from multiprocessing import shared_memory

class e_mirror():
    '''
    Effect: e_mirror

    Parameter:
    - Number of axes
    - s2l trigger On / Off
    '''

    def __init__(self):
        self.lastvalue = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.counter = 0
        self.naxis = 1
        self.trigger = False
        self.steps = 0

    def return_values(self):
        return [b'naxis', b'# of axes', b'', b'', b's2l trigger']

    def return_gui_values(self):
        if self.trigger:
            trigger = 'On'
        else:
            trigger = 'Off'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(self.naxis), '', '', trigger), 'utf-8')

    def __call__(self, world, args):
        # parsing input
        self.naxis = int(args[0]*2 +1)
        self.steps = int(args[1]*8)

        if args[3] > 0.5:
            self.trigger = True
        else:
            self.trigger = False

        tempworld = np.zeros([3, 10, 10, 10])
        tempworld[:, :, :, :] = world[:, :, :, :]

        if self.trigger:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))

            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = -1

            self.counter += 1

            if self.counter > self.steps:
                self.naxis = 0

        if self.naxis == 1:
            world[:, :, :, :] += tempworld[:, ::-1, :, :]
        elif self.naxis == 2:
            world[:, :, :, :] += tempworld[:, :, ::-1, :]
            world[:, :, :, :] += tempworld[:, :, :, ::-1]
        elif self.naxis == 3:
            world[:, :, :, :] += tempworld[:, ::-1, :, :]
            world[:, :, :, :] += tempworld[:, :, ::-1, :]
            world[:, :, :, :] += tempworld[:, :, :, ::-1]
        elif self.naxis == 0:
            pass

        return np.clip(world, 0, 1)
