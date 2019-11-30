# load modules
import numpy as np
import socket
from cube_utils import world2vox
import sys

# load generator modules
from generators.g_cube import g_cube
from generators.g_growing_sphere import g_growing_sphere
from generators.g_random import g_random
from generators.g_sphere import g_sphere
from generators.g_blank import g_blank
from generators.g_orbiter import g_orbiter
from generators.g_randomlines import g_randomlines
from generators.g_shooting_star import g_shooting_star
from generators.g_snake import g_snake
from generators.g_planes import g_planes
from generators.g_corner import g_corner
from generators.g_corner_grow import g_corner_grow
from generators.g_planes_falling import g_planes_falling
from generators.g_orbiter2 import g_orbiter2
from generators.g_wavepattern import g_wavepattern
from generators.g_randomcross import g_randomcross
from generators.g_growing_corner import g_growing_corner
from generators.g_rain import g_rain
from generators.g_pyramid import g_pyramid
from generators.g_pyramid_upsidedown import g_pyramid_upsidedown
from generators.g_circles import g_circles
from generators.g_growingface import g_growingface
from generators.g_orbiter3 import g_orbiter3
from generators.g_gauss import g_gauss
from generators.g_wave import g_wave
from generators.g_drop import g_drop
from generators.g_columns import g_columns
from generators.g_cube_edges import g_cube_edges
from generators.a_multi_cube_edges import a_multi_cube_edges
from generators.g_rotate_plane import g_rotate_plane
from generators.a_random_cubes import a_random_cubes
from generators.g_soundcube import g_soundcube
from generators.g_cut import g_cut
from generators.g_bouncy import g_bouncy
from generators.g_squares import g_squares
from generators.g_darksphere import g_darksphere
from generators.g_sound_sphere import g_sound_sphere
from generators.g_trees import g_trees
from generators.g_rising_square import g_rising_square
from generators.g_soundrandom import g_soundrandom
from generators.g_inandout import g_inandout
from generators.g_centralglow import g_centralglow
from generators.g_orbiter_big import g_orbiter_big
from generators.g_sound_grow import g_sound_grow
from generators.g_edgeglow import g_edgeglow
from generators.g_blackhole import g_blackhole
from generators.g_swell import g_swell
from generators.g_growing_square import g_growing_square
from generators.g_collision import g_collision
from generators.g_soundsnake import g_soundsnake
from generators.g_supernova import g_supernova
#from generators.a_pulsating_torus import a_pulsating_torus

# 2d cube_generators
from generators.g_2d_randomlines import g_2d_randomlines
# from generators.g_2d_moving_line import g_2d_moving_line
from generators.g_2d_growing_circle import g_2d_growing_circle
from generators.g_2d_rain import g_2d_rain
from generators.g_2d_square import g_2d_square
from generators.g_2d_portal import g_2d_portal
from generators.g_2d_random import g_2d_random
from generators.g_2d_test import g_2d_test
from generators.g_2d_conway import g_2d_conway
from generators.g_2d_orbiter import g_2d_orbiter
from generators.g_2d_patches import g_2d_patches
from generators.g_2d_random_squares import g_2d_random_squares


# vox cube_generators
from generators.g_obliqueplane import g_obliqueplane
from generators.g_obliqueplaneXYZ import g_obliqueplaneXYZ
from generators.g_falling import g_falling
from generators.g_smiley import g_smiley
from generators.g_torusrotation import g_torusrotation
from generators.g_centralglow import g_centralglow
from generators.g_rotating_cube import g_rotating_cube
from generators.g_osci_corner import g_osci_corner
from generators.g_sides import g_sides


#load effect modules
from effects.e_blank import e_blank
from effects.e_fade2blue import e_fade2blue
from effects.e_rainbow import e_rainbow
from effects.e_outer_shadow import e_outer_shadow
from effects.e_staticcolor import e_staticcolor
from effects.e_violetblue import e_violetblue
from effects.e_redyellow import e_redyellow
from effects.e_tremolo import e_tremolo
from effects.e_newgradient import e_newgradient
from effects.e_gradient import e_gradient
from effects.e_prod_saturation import e_prod_saturation
from effects.e_prod_hue import e_prod_hue
from effects.e_bright_osci import e_bright_osci
from effects.e_cut_cube import e_cut_cube
from effects.e_remove_random import e_remove_random
from effects.e_rotating_blue_orange import e_rotating_blue_orange
from effects.e_rotating_black_blue import e_rotating_black_blue
from effects.e_rotating_black_white import e_rotating_black_white
#from effects.e_sound_color import e_sound_color
from effects.e_rotating_black_red import e_rotating_black_red
from effects.e_rotating_black_orange import e_rotating_black_orange
from effects.e_s2l_shiftcolor import e_s2l_shiftcolor
from effects.e_s2l_revis import e_s2l_revis
from effects.e_average import e_average
#from effects.e_blur import e_blur
from effects.e_rare_strobo import e_rare_strobo
#from effects.e_color_silpion import e_color_silpion
from effects.e_s2l import e_s2l
from effects.e_random_brightness import e_random_brightness
from effects.e_squared import e_squared
# load automat
from generators.a_testbot import a_testbot
from generators.a_orbbot import a_orbbot
from generators.a_lines import a_lines
#from generators.a_pulsating import a_pulsating
from generators.a_jukebox import a_jukebox
from generators.a_jukebox_ambient import a_jukebox_ambient
from generators.a_squares_cut import a_squares_cut

# load effect modules
class CubeWorld:

    def __init__(self):
        # initialize worlds at startup
        # indices: [color, x, y, z]

        # world for channel A
        self.world_CHA = np.zeros([3, 10, 10, 10])
        # world for channel B
        self.world_CHB = np.zeros([3, 10, 10, 10])
        # world for channel C
        self.world_CHC = np.zeros([3, 10, 10, 10])
        #fade world for channel A
        self.world_CHA_fade = np.zeros([3, 10, 10, 10])
        #fade world for channel B
        self.world_CHB_fade = np.zeros([3, 10, 10, 10])
        #fade world for channel C
        self.world_CHC_fade = np.zeros([3, 10, 10, 10])

        # world for master
        self.world_TOT = np.zeros([3, 10, 10, 10])
        self.world_TOT_stored = np.zeros([3, 10, 10, 10])

        #channel volume
        self.amount_a=1.0
        self.amount_b=1.0
        self.amount_c=1.0
        #fade
        self.fade = 0.0
        self.brightness = 1.0

        # artnet switch
        self.switch_artnet = False
        self.switch_artnet_color = False

        self.control_dict = {}

        for i in range(150):
            self.control_dict.update( {i: 0.0} )

        self.control_dict.update({58:1})
        self.control_dict.update({62:0})

        self.CHA = []
        self.CHB = []
        self.CHC = []

        self.speed_A = 1
        self.speed_B = 1
        self.speed_C = 1

        self.fade_A = 1.0;
        self.fade_B = 1.0;
        self.fade_C = 1.0;

        # this is temporary, we need a routine to update the elements
        # in the list to change the generator/effect
        self.CHA.append(g_blank())
        self.CHA.append(e_blank())
        self.CHA.append(e_blank())
        self.CHB.append(g_blank())
        self.CHB.append(e_blank())
        self.CHB.append(e_blank())
        self.CHC.append(g_blank())
        self.CHC.append(e_blank())
        self.CHC.append(e_blank())

        # print('\nInitialize Artnet stream...\n')
        # self.artnet = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

        # self.artnet.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, 1)
        # self.artnet.settimeout(0.006) # 0.01 works
        self.artnet_universe = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


    def get_cubedata(self):
        # get vox format from the internal stored world
        # get each color
        list1 = world2vox(self.world_TOT[0, :, :, :])
        list2 = world2vox(self.world_TOT[1, :, :, :])
        list3 = world2vox(self.world_TOT[2, :, :, :])
        # put colors together in the correct order
        # this might be a speed-bottleneck? we should check
        # and do it in a faster way, numpy or else
        # liste = []
        # for i in range(1000):
        #    liste.append(list1[i])
        #    liste.append(list2[i])
        #    liste.append(list3[i])

        liste = list(np.stack((list1, list2, list3)).flatten('F'))
        return liste

    def control(self, key, value):
        # updates the control values, shift range from 0-127 to 0.0-1.0
        self.control_dict.update({key: value/127.0})

        if self.switch_artnet or self.switch_artnet_color:
            try:
                data = self.artnet.recvfrom(560)
                if sys.getsizeof(data[0]) >= 512:
                    for i in range(46,46+17):
                        self.artnet_universe[i-46] = data[0][i]/255.0
            except:
                pass


    def getParamsAndValues(self):
        return [self.CHA[0].label(),self.CHA[1].label(),self.CHA[2].label(),self.CHB[0].label(),self.CHB[1].label(),self.CHB[2].label(),self.CHC[0].label(),self.CHC[1].label(),self.CHC[2].label()]

    def getBrightnessAndShutterspeed(self):
        return['Brightness', self.amount_a,'Brightness', self.amount_b,'Brightness', self.amount_c,"Shutter", self.speed_A,"Shutter", self.speed_B,"Shutter", self.speed_C, 'Fade', self.fade_A,'Fade', self.fade_B,'Fade', self.fade_C]

    def getMasterParams(self):
        return['Master-Brightness',self.brightness, 'Master-Fade', self.fade]

    def setArtnetControl(self,bool):
        self.switch_artnet=bool
        print('ARTnet Control: '+str(self.switch_artnet))

    def setArtnetColorControl(self,bool):
        self.switch_artnet_color=bool
        print('ARTnet Color Control: '+str(self.switch_artnet_color))

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

        if self.switch_artnet == True:
            self.speed_A = int(round(self.artnet_universe[4]*30)+1)
            self.speed_B = int(round(self.artnet_universe[9]*30)+1)
            self.speed_C = int(round(self.artnet_universe[14]*30)+1)
        else:
            self.speed_A = int(round(self.control_dict[19]*30)+1)
            self.speed_B = int(round(self.control_dict[23]*30)+1)
            self.speed_C = int(round(self.control_dict[27]*30)+1)

        self.world_CHA_fade[:] = self.world_CHA
        self.world_CHB_fade[:] = self.world_CHB
        self.world_CHC_fade[:] = self.world_CHC

        self.world_CHA[:, :, :, :] = 0.0
        self.world_CHB[:, :, :, :] = 0.0
        self.world_CHC[:, :, :, :] = 0.0

        # Generator A
        if step%self.speed_A == 0:
            # Generator A
            self.CHA[0].control(self.control_dict[16],self.control_dict[17],self.control_dict[18])
            self.world_CHA = self.CHA[0].generate(step, self.world_CHA)
            # Effect A 1
            self.CHA[1].control(self.control_dict[20],self.control_dict[21],self.control_dict[22])
            self.world_CHA = self.CHA[1].generate(step, self.world_CHA)
            # Effect A 2
            self.CHA[2].control(self.control_dict[85],self.control_dict[86],self.control_dict[87])
            self.world_CHA = self.CHA[2].generate(step, self.world_CHA)

        # Generator B
        if step%self.speed_B == 0:
            # Generator B
            self.CHB[0].control(self.control_dict[24],self.control_dict[25],self.control_dict[26])
            self.world_CHB = self.CHB[0].generate(step, self.world_CHB)
            # Effect B 1
            self.CHB[1].control(self.control_dict[28],self.control_dict[29],self.control_dict[30])
            self.world_CHB = self.CHB[1].generate(step, self.world_CHB)
            # Effect B 2
            self.CHB[2].control(self.control_dict[88],self.control_dict[89],self.control_dict[90])
            self.world_CHB = self.CHB[2].generate(step, self.world_CHB)

        # Generator C
        if step%self.speed_C == 0:
            # Generator C
            self.CHC[0].control(self.control_dict[46],self.control_dict[47],self.control_dict[48])
            self.world_CHC = self.CHC[0].generate(step, self.world_CHC)
            # Effect C 1
            self.CHC[1].control(self.control_dict[50],self.control_dict[51],self.control_dict[52])
            self.world_CHC = self.CHC[1].generate(step, self.world_CHC)
            # Effect C 2
            self.CHC[2].control(self.control_dict[91],self.control_dict[92],self.control_dict[93])
            self.world_CHC = self.CHC[2].generate(step, self.world_CHC)

        '''
        if self.switch_artnet or self.switch_artnet_color:
            # overwrite colors
            self.world_CHA[0,:,:,:] *= self.artnet_universe[0]
            self.world_CHA[1,:,:,:] *= self.artnet_universe[1]
            self.world_CHA[2,:,:,:] *= self.artnet_universe[2]

            self.world_CHB[0,:,:,:] *= self.artnet_universe[5]
            self.world_CHB[1,:,:,:] *= self.artnet_universe[6]
            self.world_CHB[2,:,:,:] *= self.artnet_universe[7]

            self.world_CHC[0,:,:,:] *= self.artnet_universe[10]
            self.world_CHC[1,:,:,:] *= self.artnet_universe[11]
            self.world_CHC[2,:,:,:] *= self.artnet_universe[12]


        if self.switch_artnet:
            # brightness
            self.amount_a = self.artnet_universe[3]
            self.amount_b = self.artnet_universe[8]
            self.amount_c = self.artnet_universe[13]
            # Channel-Fade
            self.fade_A = self.control_dict[57]
            self.fade_B = self.control_dict[61]
            self.fade_C = self.control_dict[62]

            self.world_CHA = self.world_CHA + (self.world_CHA_fade * self.fade_A)
            self.world_CHB = self.world_CHB + (self.world_CHB_fade * self.fade_B)
            self.world_CHC = self.world_CHC + (self.world_CHC_fade * self.fade_C)


            # Global fade
            self.fade = self.artnet_universe[15]

            # Sum Channels
            self.world_TOT = self.amount_a * self.world_CHA + \
                            self.amount_b * self.world_CHB + \
                            self.amount_c * self.world_CHC + \
                            self.fade * self.world_TOT

            self.world_TOT = np.clip(self.artnet_universe[16] * self.world_TOT,0,0.999)

        else :
        '''
        # Channel-Brightness
        self.amount_a = self.control_dict[31]
        self.amount_b = self.control_dict[49]
        self.amount_c = self.control_dict[53]

        # Channel-Fade
        self.fade_A = self.control_dict[57]
        self.fade_B = self.control_dict[61]
        self.fade_C = self.control_dict[62]

        # Global Brightness
        self.brightness = self.control_dict[58]

        # Global fade
        self.fade = self.control_dict[59]

        self.world_CHA = self.world_CHA + (self.world_CHA_fade * self.fade_A)
        self.world_CHB = self.world_CHB + (self.world_CHB_fade * self.fade_B)
        self.world_CHC = self.world_CHC + (self.world_CHC_fade * self.fade_C)

        # Sum Channels
        self.world_TOT = self.amount_a * self.world_CHA +  \
                         self.amount_b * self.world_CHB +  \
                         self.amount_c * self.world_CHC +  \
                         self.fade * self.world_TOT_stored

        # store world without brightness applied for global fade
        self.world_TOT_stored = np.clip(self.world_TOT,0,0.999)
        # write final world
        self.world_TOT = np.clip(self.brightness * self.world_TOT,0,0.999)
