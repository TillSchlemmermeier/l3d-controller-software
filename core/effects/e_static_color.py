# modules
import numpy as np
from colorsys import hsv_to_rgb

class e_static_color():
    '''
    Effect: static color
    Parameters:
    - red
    - green
    - blue
    - HSV Hue value
    '''
    def __init__(self):
        self.red = 1.0
        self.green = 1.0
        self.blue = 1.0
        self.hsv = 0
        #self.hsv = [0.0,0.0,0.0]

    #strings for GUI
    def return_state(self):
        # return [Display Name, Viariable Name, Display Value] for each parameter
        return [
            ['Red', 'red', round(self.red,1)],
            ['Green', 'green', round(self.green,1)],
            ['Blue', 'blue', round(self.blue,1)],
            ['HSV', 'hsv', round(self.hsv,1)],    
        ]


    def __call__(self, world, args):

        self.red   = args[0]
        self.green = args[1]
        self.blue  = args[2]
        self.hsv   = args[3]
        #self.hsv[0]= args[3]

        if self.hsv > 0:
        #if self.hsv[0] > 0:
            color = hsv_to_rgb(self.hsv, 1, 1)
            #color = hsv_to_rgb(self.hsv[0], 1, 1)
            self.red   = color[0]
            self.green = color[1]
            self.blue  = color[2]

        world[0, :, :, :] *= self.red
        world[1, :, :, :] *= self.green
        world[2, :, :, :] *= self.blue

        return np.clip(world, 0, 1)
