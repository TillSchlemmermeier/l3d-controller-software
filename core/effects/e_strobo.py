from multiprocessing import shared_memory
import numpy as np

class e_strobo():

    def __init__(self):
        # parameters
        self.on = 1
        self.off = 1
        self.mode = 'rectangular'
        self.trigger = False
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.counter = 0
        self.lastvalue = 0

    def return_state(self):
        if self.trigger:
            trigger = "On"
        else:
            trigger = "Off"

        return [
            ['On', 'on', round(self.on,1)],
            ['Off', 'off', round(self.off,1)],
            ['Mode', 'mode', self.mode],
            ['Trigger', 'trigger', trigger],
        ]


    def __call__(self, world, args):
        # process parameters
        self.on = int(args[0]*9)+1
        self.off = int(args[1]*9)+1
        if args[2] <= 0.25:
            self.mode = 'rectangle'
        elif 0.25 < args[2] <= 0.5:
            self.mode = 'ramp'
        elif 0.5 < args[2] <= 0.75:
            self.mode = 'down ramp'
        else:
            self.mode = 'triangle'

        if args[3] > 0.1:
            self.trigger = True
        else:
            self.trigger = False

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
