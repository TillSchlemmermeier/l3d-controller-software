
import numpy as np
from matplotlib import colors


class e_black_color_white():

    def __init__(self):
        # parameters
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


        led_list = colors.hsv_to_rgb(hsv_list).T


        world *= np.clip(led_list.reshape([3, 10, 10, 10]),0,1)

        return np.clip(world, 0, 1)
