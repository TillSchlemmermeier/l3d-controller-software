# modules
import numpy as np
from multiprocessing import shared_memory

class e_bright_mod():
    '''
    Effect: modulation of brightness using 3D wave patterns with sound interaction
    '''

    def __init__(self):
        self.speed = 1.0
        self.amount = 0.5
        self.step = 0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 4
        self.lastvalue = 0

    def return_state(self):
        return [
            ['speed', 'speed', round(self.speed,2)],
            ['amount', 'amount', round(self.amount,2)],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.speed = args[0] * 0.1 + 0.001
        self.amount = args[1]
        self.channel = ['noS2L', 0, 1, 2, 3, 'Trigger'][round(args[2] * 5)]
        # === PARAMETERS END ===

        x = np.linspace(0,9,10)
        y = np.linspace(0,9,10)
        z = np.linspace(0,9,10)

        modulation_world = np.sum(np.meshgrid(x, y, z), axis=0)

        if isinstance(self.channel, int):
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8], 'utf-8'))
            speed_factor = self.speed * (1 + current_volume)  # Sound boosts speed
        elif self.channel == 'Trigger':
            current_volume = int(float(str(self.sound_values.buf[32:40], 'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.step = 0  # Reset step on beat
            speed_factor = self.speed
        else:
            speed_factor = self.speed

        modulation_world = 0.5 * np.sin(modulation_world * self.step * speed_factor) + 0.5

        for i in range(3):
            world[i] -= modulation_world * self.amount

        self.step += 1

        return np.clip(world, 0, 1)
