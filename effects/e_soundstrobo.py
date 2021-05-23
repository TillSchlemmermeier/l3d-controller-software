from multiprocessing import shared_memory
import numpy as np

class e_soundstrobo():


    def __init__(self):
        # parameters
        self.channel = 1
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.counter = 0
        self.lastvalue = 0
        self.mode = 'normal'
        self.amount = 1

    def return_values(self):
        # strings for GUI
        return [b'soundstrobo', b'amount', b'mode', b'', b'channel']

    def return_gui_values(self):
        if self.channel < 4:
            channel = str(self.channel)
        else:
            channel = "Trigger"

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,1)), self.mode, '', channel) ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        self.amount = int(args[0]*12)
        if args[1] < 0.5:
            self.mode = 'normal'
        else:
            self.mode = 'invert'
        self.channel = int(args[3]*4)

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


            if self.mode == 'normal':
                if self.counter < self.amount:
                    if self.counter % 2 == 0:
                        world[:, :, :, :] = 0
                    self.counter += 1
                else:
                    self.counter += 1
            else:
                if self.counter < self.amount:
                    if self.counter % 2 != 0:
                        world[:, :, :, :] = 0
                    self.counter += 1
                else:
                    world[:, :, :, :] = 0
                    self.counter += 1


            self.lastvalue = current_volume


        return np.clip(world, 0, 1)
