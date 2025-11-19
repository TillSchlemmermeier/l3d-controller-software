import numpy as np
from multiprocessing import shared_memory

class e_break_fade():
    '''Effect: Fade during beat breaks, optional S2L brightness during beats'''

    def __init__(self):
        self.fade = 0.0
        self.s2l = 0.0
        self.timeout = 15  # frames without trigger before fading starts
        self.sound_values = shared_memory.SharedMemory(name="global_s2l_memory")
        self.lastworld = np.zeros([3, 10, 10, 10])
        self.lastvalue = 0
        self.frames_since_trigger = 0

    def return_state(self):
        return [
            ['fade in break', 'fade', round(self.fade, 2)],
            ['s2l in beat', 's2l', round(self.s2l, 2)],
        ]

    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.fade = args[0]
        self.s2l = args[1]
        # === PARAMETERS END ===

        current_volume = int(float(str(self.sound_values.buf[32:40], 'utf-8')))

        if current_volume > self.lastvalue:
            self.lastvalue = current_volume
            self.frames_since_trigger = 0
        else:
            self.frames_since_trigger += 1

        # in break
        if self.frames_since_trigger >= self.timeout:
            world = world + self.lastworld * self.fade
        # during beats
        else:
            if self.s2l:
                current_volume = float(str(self.sound_values.buf[0:8], 'utf-8'))
                world *= 1 - (current_volume * self.s2l)

        self.lastworld[:, :, :, :] = world[:, :, :, :]

        return np.clip(world, 0, 1)
