# modules
import numpy as np
from colorsys import hsv_to_rgb
from scipy.ndimage.interpolation import rotate

class e_rotating_rainbow():

    def __init__(self):

        # initial rotating parameters
        self.speed = 0
        self.rotation = 0.1
        self.gradient_length = 1.0
        self.step = 1
        self.rotX = 1
        self.rotYZ = 1

    #strings for GUI
    def return_values(self):
        return [b'rotating_rainbow', b'Length', b'Speed', b'Rot_X', b'Rot_YZ']

    def return_gui_values(self):
        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(10 * self.speed,2)), str(round(self.gradient_length,1)), str(round(self.rotX,1)), str(round(self.rotYZ,1))), 'utf-8')

    def __call__(self, world, args):
		# parse input
        self.speed = args[0]*0.1
        self.gradient_length = args[1]
        self.rotX = args[2]*15+0.01
        self.rotYZ = args[3]*15+0.01

        # create gradient
        self.rainbowworld = np.zeros([3, 10, 10, 10])

        for i in range(3):
            for j in range (10):
                self.rainbowworld[i, j, :, :] = hsv_to_rgb((j / 10) * self.gradient_length + self.step * self.speed, 1, 1)[i]

        # rotate
        newworld = rotate(self.rainbowworld, self.step*self.rotX,
                          axes = (1,2), order = 1,
                          mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.rotYZ,
                          axes = (1,3), order = 1,
                          mode = 'nearest', reshape = False)

        newworld = rotate(newworld, self.step*self.rotYZ,
                          axes = (2,3), order = 1,
                          mode = 'nearest', reshape = False)

        world *= newworld
        self.step += 1

        return np.clip(world, 0, 1)
