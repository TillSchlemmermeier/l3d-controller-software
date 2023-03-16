
import numpy as np
from multiprocessing import shared_memory

class e_s2l():

    def __init__(self):
        # parameters
        self.amount = 1.0
        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastvalue = 0
        self.counter = 0
        self.step = 8
        self.mode = 'normal'
        self.decay = 0
        self.value = 0.0

    def return_values(self):
        # strings for GUI
        return [b's2l', b'amount', b'channel', b'mode', b'decay']

    def return_gui_values(self):
        if self.channel < 4:
            channel = str(self.channel)
        elif self.channel == 4:
            channel = "Trigger"
        else:
            channel = 'Trig 2'

        if self.decay == 0:
            decay = 'off'
        else:
            decay = str(self.decay)

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount,1)), channel, self.mode,decay) ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        self.amount = args[0]
        self.channel = int(args[1]*5)
        if args[2] > 0.5:
            self.mode = 'invert'
        else:
            self.mode = 'normal'

        self.decay = round(args[3]*0.5,2)


        # apply manipulation
        if self.channel < 4:

            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))**4

            if self.decay == 0:
                world[:, :, :, :] *= (1-self.amount) + np.clip(current_volume,0,1)*self.amount
            else:
                if current_volume > self.value:
                    self.value = current_volume
                elif self.value == 0:
                    world[:, :, :, :] *= 0
                else:
                    self.value = np.clip(self.value * (1-self.decay), 0, 1)
                    world[:, :, :, :] *= (1-self.amount) + self.value*self.amount

        else:
            # trigger normal
            if self.channel == 4:
                current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
                if current_volume > self.lastvalue:
                    self.lastvalue = current_volume
                    self.counter = 0

            # trigger half
            elif self.channel == 5:
                current_volume = int(float(str(self.sound_values.buf[40:48],'utf-8')))
                if current_volume == 1:
                    self.lastvalue = current_volume
                    self.counter = 0

            if self.mode == 'normal':

                # old stuff
                if self.counter < self.step:
                    world[:, :, :, :] *= (1 - self.amount) + ((self.step - self.counter) / self.step) * self.amount
            else:
                # if self.counter < 20:
                #     pass
                if 15 < self.counter: # < (self.step + 1000)
#                    print(self.counter ,(self.counter-15)/(self.step + 100))
                    world[:, :, :, :] *= ((self.counter-15)/(self.step + 100))
                #elif self.counter > (self.step + 100):
                #    world[:, :, :, :] = 0.0
                else:
                    world[:, :, :, :] = 0.0
            self.counter += 1


        return np.clip(world, 0, 1)
