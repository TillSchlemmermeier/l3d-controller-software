# modules
import numpy as np

class g_edgelines():

    def __init__(self):
        self.counter = 0


    def return_values(self):
        # Strings for GUI
        return [b'edgelines', b'', b'', b'', b'']


    def __call__(self, args):

        world = np.zeros([3, 10, 10, 10])

        # down
        if self.counter <= 10:
            world[:, :self.counter, 0, 0] = 1.0
            world[:, :self.counter, 9, 9] = 1.0
        elif self.counter > 10 and self.counter <= 20:
            world[:, self.counter-10:, 0, 0] = 1.0
            world[:, self.counter-10:, 9, 9] = 1.0
        # side
        elif self.counter > 20 and self.counter <= 30:
            world[:, 9, :self.counter-30, 0] = 1.0
            world[:, 9, 0, :self.counter-30] = 1.0
            world[:, 9, 10-(self.counter-20):, 9] = 1.0
            world[:, 9, 9, 10-(self.counter-20):] = 1.0
        elif self.counter > 30 and self.counter <= 40:
            world[:, 9, self.counter-31:, 0] = 1.0
            world[:, 9, 0, self.counter-31:] = 1.0
            world[:, 9, :9-(self.counter-20), 9] = 1.0
            world[:, 9, 9, :9-(self.counter-20)] = 1.0
        # up
        elif self.counter > 40 and self.counter <= 50:
            world[:, 10-(self.counter-40):, 9, 0] = 1.0
            world[:, 10-(self.counter-40):, 0, 9] = 1.0
        elif self.counter > 50 and self.counter <= 60:
            world[:, :10-(self.counter-50), 9, 0] = 1.0
            world[:, :10-(self.counter-50), 0, 9] = 1.0
        # side
        elif self.counter > 60 and self.counter <= 70:
            world[:, 0, 0, 10-(self.counter-60):] = 1.0
            world[:, 0, 10-(self.counter-60):, 0] = 1.0
            world[:, 0, :self.counter-60, 9] = 1.0
            world[:, 0, 9, :self.counter-60] = 1.0
        elif self.counter > 70 and self.counter <= 80:
            world[:, 0, 0, :9-(self.counter-60)] = 1.0
            world[:, 0, :9-(self.counter-60), 0] = 1.0
            world[:, 0, self.counter-70:, 9] = 1.0
            world[:, 0, 9, self.counter-70:] = 1.0
        else:
            self.counter = 0

        self.counter += 1

        return np.clip(world, 0, 1)
