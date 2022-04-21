
import numpy as np
from multiprocessing import shared_memory
from matplotlib import colors

class e_soundhsv():

    def __init__(self):
        # parameters
        self.amount_h = 0.0
        self.amount_s = 0.0
        self.amount_v = 0.0
        self.channel = 1.0
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.lastvalue = 0
        self.counter = 0
        self.step = 8
        self.mode = 'normal'

    def return_values(self):
        # strings for GUI
        return [b'sound hsv', b'amount hue', b'amount sat', b'amount val', b'channel']

    def return_gui_values(self):
        if self.channel < 4:
            channel = str(self.channel)
        else:
            channel = "Trigger"

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.amount_h,1)), str(round(self.amount_s,1)), str(round(self.amount_v,1)),channel) ,'utf-8')

    def __call__(self, world, args):
        # process parameters
        self.channel = int(args[3]*3)


        self.amount_h = round(args[0]*1.8 - 0.9, 1)
        self.amount_s = round(args[1]*1.8 - 0.9, 1)
        self.amount_v = round(args[2]*1.8 - 0.9, 1)

        # get sound
        current_volume = 0.5*float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))**4

        # get list of leds
        led_list = world.reshape([3, 10**3]).T

        hsv_list = colors.rgb_to_hsv(led_list)
        # print(round(self.amount_h*current_volume, 2), round(self.amount_s*current_volume, 2))

        hsv_list[:, 0] += np.clip(self.amount_h * current_volume, -1, 1)
        hsv_list[:, 1] += np.clip(self.amount_s * current_volume, -1, 1)
        hsv_list[:, 2] += np.clip(self.amount_v * current_volume, -1, 1)

        led_list = colors.hsv_to_rgb(hsv_list).T

        world = led_list.reshape([3, 10, 10, 10])

        return np.clip(world, 0, 1)
