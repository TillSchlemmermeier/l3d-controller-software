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
        self.CHA.append(g_cube())
        self.CHB.append(g_cube())

    def get_cubedata(self):
        # get vox format from internal stored world

        # get each color
        list1 = world2vox2(self.world_TOT[0, :, :, :])
        list2 = world2vox2(self.world_TOT[1, :, :, :])
        list3 = world2vox2(self.world_TOT[2, :, :, :])

        # put colors together
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
        self.world_CHA = self.CHA[0].generate(step)
        # Generators
        # Effects

        # Channel B
        # Generators
        # Effects

        # Sum Channels
        self.world_TOT = self.world_CHA + self.world_CHB
        # np.round(np.clip(world, 0, 1), 3)
        # self.world_TOT = np.clip(round(self.world_TOT,3),0,1)
        # or self.world_TOT += self.world_CHA + self.world_CHB?

        # Global Effects
