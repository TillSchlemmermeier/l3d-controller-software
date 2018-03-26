# load modules
import numpy as np
from cube_utils import world2vox2

# load generator modules
from g_cube import g_cube
from g_growing_sphere import g_growing_sphere
from g_random import g_random
from g_sphere import g_sphere
from g_randomlines import g_randomlines
# load effect modules


class CubeWorld:

    def __init__(self):
        # initialize worlds at startup
        # indices: [color, x, y, z]

        # world for channel A
        self.world_CHA = np.zeros([3, 10, 10, 10])
        # world for channel B
        self.world_CHB = np.zeros([3, 10, 10, 10])
        # world for master
        self.world_TOT = np.zeros([3, 10, 10, 10])

        # self.framecounter = 0

        self.control_dict = {}

        for i in range(150):
            self.control_dict = {i: 0.0}

        self.CHA = []
        self.CHB = []

        # this is temporary, we need a routine to update the elements
        # in the list to change the generator/effect
        self.CHA.append(g_cube())
        self.CHB.append(g_cube())

    def get_cubedata(self):
        # get vox format from the internal stored world

        # get each color
        list1 = world2vox2(self.world_TOT[0, :, :, :])
        list2 = world2vox2(self.world_TOT[1, :, :, :])
        list3 = world2vox2(self.world_TOT[2, :, :, :])

        # put colors together in the correct order
        # this might be a speed-bottleneck? we should check
        # and do it in a faster way, numpy or else
        liste = []
        for i in range(1000):
            liste.append(list1[i])
            liste.append(list2[i])
            liste.append(list3[i])

        return liste

    def control(self, key, value):
        # updates the control values
        self.control_dict.update({key: value})

    def set_Genenerator(self, generator, name):
        fullFunction = "self.CH"+generator+"[0]="+name+"()"
        exec(fullFunction)

    def test_screen(self, clear=True):
        # creates a test_screen to check orientation
        # and proper colours

        # clears world matrices if clear == True
        if clear:
            self.world_CHA[:, :, :, :] = 0
            self.world_CHB[:, :, :, :] = 0
            self.world_TOT[:, :, :, :] = 0

        # draw something in the red channel
        # of channel A
        self.world_CHA[0, :1, 0, 0] = 1
        self.world_CHA[0, 0, :2, 0] = 1
        self.world_CHA[0, 0, 0, :3] = 1

        # draw something in the blue channel
        # of channel B
        self.world_CHB[2, 0, 0, 0] = 1
        self.world_CHB[2, 9, 0, 0] = 1
        self.world_CHB[2, 0, 9, 0] = 1
        self.world_CHB[2, 0, 0, 9] = 1
        self.world_CHB[2, 0, 9, 9] = 1
        self.world_CHB[2, 9, 0, 9] = 1
        self.world_CHB[2, 9, 9, 0] = 1
        self.world_CHB[2, 9, 9, 9] = 1

    def update(self, step):
        # updates the world matrices according
        # to assigned generators and filters

        # Channel A
        # loop over each element in CHA and perform thier 'generate'
        # routine. now, the first element is always the generator around
        # the second can be an effect, but in principle this supports an
        # unlimited number of generators and effects on one channel.
        # This also determines, that the input of each generate function
        # must always be defined as <somegenerator.generate>(self, step, world)
        for i in self.CHA:
            self.world_CHA = i.generate(step, self.world_CHA)

        # Channel B
        for i in self.CHB:
            self.world_CHB = i.generate(step, self.world_CHB)

        # Sum Channels
        self.world_TOT = np.clip(amount_a * self.world_CHA + \
                                 amount_b * self.world_CHB + \
                                 fade * self.world_TOT, 0, 1)

        # Global Effects
        # the global fade is already included at the "sum channels"
