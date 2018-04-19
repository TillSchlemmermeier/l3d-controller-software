# load modules
import numpy as np
from cube_utils import world2vox

# load generator modules
from g_cube import g_cube
from g_growing_sphere import g_growing_sphere
from g_random import g_random
from g_sphere import g_sphere
from g_blank import g_blank
from g_orbiter import g_orbiter
from g_randomlines import g_randomlines
from g_shooting_star import g_shooting_star
from g_snake import g_snake
#load effect modules
from e_blank import e_blank
from e_fade2blue import e_fade2blue
from e_rainbow import e_rainbow
from e_staticcolor import e_staticcolor
#from g_randomlines import g_randomlines
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
        #channel volume
        self.amount_a=1.0
        self.amount_b=1.0
        #fade
        self.fade = 0.0

        # self.framecounter = 0

        self.control_dict = {}

        for i in range(150):
            self.control_dict.update( {i: 0.0} )

        self.CHA = []
        self.CHB = []

        self.speed_A = 1
        self.speed_B = 1

        # this is temporary, we need a routine to update the elements
        # in the list to change the generator/effect
        self.CHA.append(g_blank())
        self.CHA.append(e_blank())
        self.CHB.append(g_blank())
        self.CHB.append(e_blank())

    def get_cubedata(self):
        # get vox format from the internal stored world
        # get each color
        list1 = world2vox(self.world_TOT[0, :, :, :])
        list2 = world2vox(self.world_TOT[1, :, :, :])
        list3 = world2vox(self.world_TOT[2, :, :, :])
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
        # updates the control values, shift range from 0-127 to 0.0-1.0
        self.control_dict.update({key: value/127.0})

    def set_Genenerator(self, generator, name, key):
        fullFunction = "self.CH"+generator+"["+str(key)+"]="+name+"()"
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

        self.speed_A = int(round(self.control_dict[49]*20)+1)
        self.speed_B = int(round(self.control_dict[53]*20)+1)

        self.world_CHA[:, :, :, :] = 0.0
        self.world_CHB[:, :, :, :] = 0.0

        # Generator A
        if step%self.speed_A == 0:
            # Generator A
            self.CHA[0].control(self.control_dict[16],self.control_dict[17],self.control_dict[18])
            self.world_CHA = self.CHA[0].generate(step, self.world_CHA)
            # Effect A
            self.CHA[1].control(self.control_dict[20],self.control_dict[21],self.control_dict[22])
            self.world_CHA = self.CHA[1].generate(step, self.world_CHA)


        #Brightness A
        self.amount_a = self.control_dict[57]


        if step%self.speed_B == 0:
            # Generator B
            self.CHB[0].control(self.control_dict[24],self.control_dict[25],self.control_dict[26])
            self.world_CHB = self.CHB[0].generate(step, self.world_CHB)
            # Effect B
            self.CHB[1].control(self.control_dict[28],self.control_dict[29],self.control_dict[30])
            self.world_CHB = self.CHB[1].generate(step, self.world_CHB)

        #Brightness B
        self.amount_b = self.control_dict[61]

        #Global fade
        self.fade = self.control_dict[62]

        # Sum Channels
        self.world_TOT = np.clip(self.amount_a * self.world_CHA + \
                                 self.amount_b * self.world_CHB + \
                                 self.fade * self.world_TOT, 0, 1)

        # Global Effects
        # the global fade is already included at the "sum channels"
