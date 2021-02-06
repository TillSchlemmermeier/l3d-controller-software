from multiprocessing import shared_memory
import numpy as np

class e_soundstrobo():


    def __init__(self):
        # parameters
        self.amount = 1.0
        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.counter = 0
        self.channel = 4
        self.lastvalue = 0
        self.steps = 1

    def return_values(self):
        # strings for GUI
        return [b'soundstrobo', b'amount', b'channel', b'strobesteps', b'']

    def return_gui_values(self):
        if self.channel < 4:
            channel = str(self.channel)
        else:
            channel = "Trigger"

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,1)), channel, str(round(self.steps,1)),'') ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        self.amount = args[0]
        self.channel = int(args[1]*4)
        self.steps = int(args[2]*10)

        # apply manipulation
        if self.channel < 4:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))**4
            if current_volume > 0.5:
                if self.counter == 0:
                    world[:, :, :, :] = 0
                    self.counter += 1
                else:
                    self.counter = 0
        else:
            current_volume = int(float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8')))
            if current_volume > self.lastvalue:
                self.counter = 0

            if self.counter < self.steps:
                if self.counter % 2 == 0:
                    world[:, :, :, :] = 0
                self.counter += 1
            else:
                self.counter += 1

            self.lastvalue = current_volume


        return np.clip(world, 0, 1)
