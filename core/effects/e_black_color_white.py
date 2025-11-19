
import numpy as np
from multiprocessing import shared_memory
from matplotlib import colors
from colorsys import hsv_to_rgb, rgb_to_hsv


class e_black_color_white():

    def __init__(self):
        # parameters
        self.amount_h = 0.0
        self.amount_s = 0.0
        self.amount_v = 0.0
        self.channel = 1.0
        self.lastvalue = 0
        self.counter = 0
        self.step = 0
        self.mode = 'normal'
        self.damping = 0.0
        self.color = 0.0

    def return_state(self):
        return [
            ['color', 'color', round(self.color,1)],
            ['damping', 'damping', round(self.damping,1)],
        ]
    
    def __call__(self, world, args):
        # === PARAMETERS START ===
        self.color   = args[0]
        self.damping = args[1]*0.5
        # === PARAMETERS END ===


        # get average brigthness
        temp = np.mean(world, axis = 0)

        world *= 1 - self.damping

        # get list of leds
        led_list = temp.reshape(10**3).T

        saturation = 1 - np.clip(led_list*2-1, 0, 1)

        brightness = np.clip(led_list*2, 0, 1)**2

        hsv_list = np.array([10**3*[self.color], saturation, brightness]).T


        #inds = np.where(hsv_list[:, 2] > 0)[0]
        #hsv_list[inds, 0] += np.clip(self.amount_h * current_volume, 0, 1)
        #hsv_list[inds, 1] += np.clip(self.amount_s * current_volume, -1, 1)
        #hsv_list[inds, 2] += np.clip(self.amount_v * current_volume, -1, 1)

        led_list = colors.hsv_to_rgb(hsv_list).T


        world *= np.clip(led_list.reshape([3, 10, 10, 10]),0,1)

        #self.step += 1

        return np.clip(world, 0, 1)
