from multiprocessing import shared_memory
import numpy as np

class e_strobo():

    def __init__(self):
        # parameters
        self.on = 1
        self.off = 1
        self.mode = 'rectangular'
        self.trigger = 'Off'
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.counter = 0
        self.lastvalue = 0

    def return_state(self):
        return [
            ['On', 'on', round(self.on,1)],
            ['Off', 'off', round(self.off,1)],
            ['Mode', 'mode', self.mode],
            ['Trigger', 'trigger', 'On' if self.trigger else 'Off'],
        ]


    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.on = int(args[0]*9)+1
        self.off = int(args[1]*9)+1
        self.mode = ['rectangle', 'ramp', 'down ramp', 'triangle'][round(args[2]*3)]
        self.trigger = args[3] > 0.5
        # === PARAMETERS END ===

        # apply manipulation
        if self.trigger:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = 0


        if self.counter <= self.on:
            if self.mode == 'ramp':
                world[:, :, :, :] *= (self.counter / self.on)
            elif self.mode == 'down ramp':
                world[:, :, :, :] *= ((self.on - self.counter) / self.on)
            elif self.mode == 'triangle':
                if self.counter <= self.on/2:
                    world[:, :, :, :] *= (self.counter / (self.on / 2))
                else:
                    world[:, :, :, :] *= (self.on - self.counter) / (self.on / 2)

            self.counter += 1

        else:
            world[:, :, :, :] = 0

            if not self.trigger:
                self.counter += 1
                if self.counter > (self.on + self.off):
                    self.counter = 0

        return np.clip(world, 0, 1)
