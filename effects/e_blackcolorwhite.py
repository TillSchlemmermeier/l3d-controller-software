
import numpy as np
from multiprocessing import shared_memory
from matplotlib import colors
from colorsys import hsv_to_rgb, rgb_to_hsv


class e_blackcolorwhite():

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

    def return_values(self):
        # strings for GUI
        return [b'blackcolorwhite', b'', b'', b'', b'']

    def return_gui_values(self):
        if self.channel < 4:
            channel = str(self.channel)
        else:
            channel = "Trigger"

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.color,1)), '', '','') ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        self.channel = int(args[3]*3)
        #self.color   = hsv_to_rgb(args[0], 1, 1)
        self.color   = args[0]


        # get average brigthness
        temp = np.mean(world, axis = 0)

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
