
import numpy as np
import logging
from channel import class_channel

# load shots
from oneshots.s_sides import *
from oneshots.s_blank import *
from oneshots.s_fade import *
from oneshots.s_dark import *
from oneshots.s_growing_sphere import *
from oneshots.s_roll import *
from oneshots.s_strobo import s_strobo
from oneshots.s_cubes import s_cubes
from oneshots.s_dark_sphere import s_dark_sphere

import time


file = open("effects.dat", "r")
effectsFile = file.readlines()
for effect in effectsFile:
    exec('from effects.' + str(effect).replace('\n','') + ' import *')

class rendering_engine_visualization:
    """
    L3D Cube 4.0

    class for the rendering engine
    """
    def __init__(self, state, log=False):
        """
        Initialises the rendering engine

        Keywords:
        log : enables logging on the debug label
              if false, the rendering engine is logging,
              but only errors/warnings
        """
        # initialise variables
        self.framecounter = 1
        self.logging = log
        self.debug = False     # debugging mode, switches  on if no arduino is found

        self.header = [int(66),
                       int(69),
                       int(69),
                       int(70)]

        # take care of logging
        if self.logging:
            logging.basicConfig(filename='log_rendering_enginge.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(message)s')
        else:
            logging.basicConfig(filename='log_rendering_enginge.log',
                                level=logging.INFO,
                                format="%(asctime)s %(message)s")

        logging.info('Variables initialised')

        # initialize global effects
        self.global_effects = []

        # Initialize timing variables
        self.start_time = time.time()
        self.frame_count = 0

        # one shots
        self.shot_state = 0
        self.shot = s_blank()
        self.shot_list = []
        self.shot_list.append(s_blank)
        self.shot_list.append(s_sides)
        self.shot_list.append(s_fade)
        self.shot_list.append(s_dark)
        self.shot_list.append(s_growing_sphere)
        self.shot_list.append(s_roll)
        self.shot_list.append(s_strobo)
        self.shot_list.append(s_cubes)
        self.shot_list.append(s_dark_sphere)

        # setup empty world
        self.cubeworld = np.zeros([3, 10, 10, 10])
        self.channelworld = np.zeros([8, 3, 10, 10, 10])

        # initialise channels
        self.channels = []
        for i in range(1,9):
            self.channels.append(class_channel(i))

        logging.warning('Initialisation complete')

    def run(self, state):
        """generates a frame and sends the package when cube is turned on"""
        # check wether 'running' flag is set
        if state['IO'] == 1:
            self.generate_frame(state)
            self.framecounter += 1

            # Prepare combined cube data
            cube_colors = np.zeros([4, 1000])
            cube_colors[0, :] = self.cubeworld[0, :, :, :].flatten()
            cube_colors[1, :] = self.cubeworld[1, :, :, :].flatten()
            cube_colors[2, :] = self.cubeworld[2, :, :, :].flatten()
            cube_colors[3, :] = 1.0

            # Prepare channel data
            channel_colors = np.zeros([8, 4, 1000])  # 8 channels, 4 color components (RGB + alpha), 1000 LEDs
            for i in range(8):
                channel_colors[i, 0, :] = self.channelworld[i, 0, :, :, :].flatten()  # R
                channel_colors[i, 1, :] = self.channelworld[i, 1, :, :, :].flatten()  # G
                channel_colors[i, 2, :] = self.channelworld[i, 2, :, :, :].flatten()  # B
                channel_colors[i, 3, :] = 1.0  # Alpha

        else:
            colors = np.zeros([4, 1000])
            channel_colors = np.zeros([8, 4, 1000])


        # Increment frame count
        self.frame_count += 1

        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time

        # Print the frequency every second
        if elapsed_time >= 10.0:
            print(f"Run method executed {self.frame_count} times in the last 10 seconds")
            self.frame_count = 0
            self.start_time = time.time()

        # Combine all data into a single array with cube_colors as first element
        # Reshape cube_colors and channel_colors to have consistent dimensions
        cube_colors_reshaped = cube_colors.T.reshape(1, 1000, 4)  # Shape: (1, 1000, 4)
        channel_colors_reshaped = channel_colors.transpose(0, 2, 1)  # Shape: (8, 1000, 4)
        
        # Concatenate along first axis
        all_colors = np.concatenate([cube_colors_reshaped, channel_colors_reshaped], axis=0)  # Shape: (9, 1000, 4)

        return all_colors

    def send_frame(self):
        """
        Function to convert world to voxel format,
        and send it through serial interface to the
        Arduino
        """

        package = bytearray(self.header + self.get_cubedata())
        # self.arduino.write(package)

        # if not self.debug:
        #     self.arduino.write(bytearray(package))
        #
        # else:
        #     logging.info('Frame '+str(self.framecounter))
        #     logging.info(package)

    def generate_frame(self, state):
        """
        Calculates a new frame according to the
        entries in the global parameter variable

        writes the result into self.cubeworld
        """
        number_of_channels = state['numberOfChannels']
        # loop through channels
        for i in range(number_of_channels):
            channel = self.channels[i]
            this_channel = state[i]
            # check if channel needs to be updated
            if this_channel['update'] == 1:
                this_channel = channel.update_channel(this_channel)
                this_channel['update'] = 0
                state[i] = this_channel
            # check whether channel is active
            if this_channel['IO'] == 1:
                # calculate frame
                new_world = channel.render_frame(self.framecounter, this_channel)
            # otherwise overrides channel world with zeros
            else:
                new_world = np.zeros([3, 10, 10, 10])

            # apply channel fade
            self.channelworld[i, :, :, :] = new_world + this_channel['fade']*\
                                             self.channelworld[i, :, :, :]

        # calculate brightness for channels
        channel_brightness = [
            np.clip(state[i]['brightness'], 0, state['brightness-limiter'])
            for i in range(number_of_channels)
        ]

        # Apply global fade
        self.cubeworld *= state['fade']

        # copy channels together
        for i in range(number_of_channels):
            self.cubeworld += channel_brightness[i] * self.channelworld[i, :, :, :]

        # check if global effects need to be updated
        if state[9]['update'] == 1:
            state[9] = self.update_global_effects(state[9])

        # apply global effect 
        for i in range(len(state[9]['effects'])):
            self.cubeworld = self.global_effects[i](self.cubeworld, state[9]['effects'][i]['params'][3::4])


        # detect whether a oneshot is fired
        # if self.global_parameter[220] > 0:
        #     self.shot_state = self.global_parameter[220]
        #     self.shot = self.shot_list[int(self.shot_state)]()
        #     self.global_parameter[220] = 0

        # if self.shot_state > 0:
        #     self.cubeworld, counter = self.shot(self.cubeworld)
        #     if counter <= 0:
        #         self.shot_state = 0
        #         self.shot = s_blank()

        # adjust global brightness
        self.cubeworld *= state['brightness']


    def update_global_effects(self, globalEffects):
        numEffects = len(globalEffects['effects'])
        # if global effects were removed, remove them from the list
        if numEffects < len(self.global_effects):
            self.global_effects = self.global_effects[:numEffects]

        # check if global effects need to be updated and if so, loop over them
        for i in range(numEffects):
            this_effect = globalEffects['effects'][i]
            if this_effect['update'] == 1:
                # if the effect was added, add a new instance to the list
                if i >= len(self.global_effects):
                    exec('self.global_effects.append(' + this_effect['name'] + '())')
                # otherwise check if effect changed and if so, replace old effect with instance of the new one
                elif this_effect['name'] != self.global_effects[i].__class__.__name__:
                    exec('self.global_effects[i] = ' + this_effect['name'] + '()')

                # check if a preset was loaded and if not, initialise the params array with zeros
                if not this_effect['params']:
                    params = []
                    for i in range(4 * len(self.global_effects[i].return_state())):
                        params.append(0)
                    this_effect['params'] = params

            # update the effect parameters in the state with current values, leave the MIDI values
            effect_state = self.global_effects[i].return_state()
            for j in range(len(effect_state)):
                this_effect['params'][4*j:4*j+3] = effect_state[j][:3]
            this_effect['update'] = 0
            globalEffects['effects'][i] = this_effect
        globalEffects['update'] = 0
        return globalEffects