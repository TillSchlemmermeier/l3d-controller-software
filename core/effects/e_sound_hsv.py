import struct
import numpy as np
from multiprocessing import shared_memory
from matplotlib import colors

class e_sound_hsv():

    def __init__(self):
        # parameters
        self.amount_h = 0.0
        self.amount_s = 0.0
        self.amount_v = 0.0
        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastvalue = 0
        self.counter = 0
        self.step = 0
        self.mode = 'normal'

    def return_state(self):
        return [
            ['amount hue', 'amount_h', round(self.amount_h,1)],
            ['amount sat', 'amount_s', round(self.amount_s,1)],
            ['amount val', 'amount_v', round(self.amount_v,1)],
            ['channel', 'channel', self.channel],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount_h = round(args[0]*0.5, 1)
        self.amount_s = round(args[1]*2 - 1.0, 1)
        self.amount_v = round(args[2]*1.8 - 0.9, 1)
        self.channel = int(args[3]*3)
        # === PARAMETERS END ===

        # get sound
        current_volume = 0.2*struct.unpack('d', bytes(self.sound_values.buf[self.channel*8:self.channel*8+8]))[0]**4
        if current_volume > self.lastvalue:
            self.lastvalue = np.clip(current_volume,0,1)
        else:
            self.lastvalue = np.clip(self.lastvalue - 0.2, 0,1)
        #current_volume = 0.5*np.sin(self.step * 0.1) + 0.5

        # get list of leds
        led_list = world.reshape([3, 10**3]).T

        hsv_list = np.round(colors.rgb_to_hsv(np.clip(led_list, 0, 1)),2)
        # print(round(self.amount_h*current_volume, 2), round(self.amount_s*current_volume, 2))

        inds = np.where(hsv_list[:, 2] > 0)[0]
        hsv_list[inds, 0] += np.clip(self.amount_h * self.lastvalue, 0, 1)
        hsv_list[inds, 1] += np.clip(self.amount_s * self.lastvalue, -1, 1)
        hsv_list[inds, 2] += np.clip(self.amount_v * self.lastvalue, -1, 1)

        led_list = colors.hsv_to_rgb(hsv_list).T

        world = led_list.reshape([3, 10, 10, 10])

        #self.step += 1

        return np.clip(world, 0, 1)
