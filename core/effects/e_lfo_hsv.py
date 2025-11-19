
import numpy as np
from multiprocessing import shared_memory
from matplotlib import colors

class e_lfo_hsv():

    def __init__(self):
        # parameters
        self.amount_h = 0.0
        self.amount_s = 0.0
        self.amount_v = 0.0
        self.speed = 1.0
        self.counter = 0

    def return_state(self):
        return [
            ['amount hue', 'amount_h', round(self.amount_h,1)],
            ['amount sat', 'amount_s', round(self.amount_s,1)],
            ['amount val', 'amount_v', round(self.amount_v,1)],
            ['speed', 'speed', round(self.speed,1)],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.amount_h = round(args[0]*0.5, 1)
        self.amount_s = round(args[1]*2 - 1.0, 1)
        self.amount_v = round(args[2]*1.8 - 0.9, 1)
        self.speed = args[3]*3+1E-2
        # === PARAMETERS END ===

        current_volume = np.sin(0.1*self.speed * self.counter)+1

        # get list of leds
        led_list = np.round(world.reshape([3, 10**3]).T,2)

        hsv_list = colors.rgb_to_hsv(led_list)
        # print(round(self.amount_h*current_volume, 2), round(self.amount_s*current_volume, 2))

        inds = np.where(hsv_list[:, 2] > 0)[0]
        hsv_list[inds, 0] += np.clip(self.amount_h * current_volume, -1, 1)
        hsv_list[inds, 1] += np.clip(self.amount_s * current_volume, -1, 1)
        hsv_list[inds, 2] += np.clip(self.amount_v * current_volume, -1, 1)

        led_list = colors.hsv_to_rgb(hsv_list).T

        world = led_list.reshape([3, 10, 10, 10])

        self.counter += 1

        return np.clip(world, 0, 1)
