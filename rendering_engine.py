
import numpy as np
import logging
import serial
from world2vox_fortran import world2vox_f as world2vox
#from global_parameter_module import global_parameter
from channel import class_channel
#from convert_dict import converting_dict

class rendering_engine:
    """
    L3D Cube 3.0

    class for the rendering engine

    assuming a global variable called
    'global_parameter':
    - numpy array with size of 255
    - entries ordered as described in
      readme
    """
    def __init__(self, array, log=False):
        """
        Initialises the rendering engine

        Keywords:
        log : enables logging on the debug label
              if false, the rendering engine is logging,
              but only errors/warnings
        """

        # initialise variables
        self.framecounter = 0
        self.logging = log
        self.debug = False          # debugging mode, switches on if no
                                    # arduino is found
        self.header = [int(66),
                       int(69),
                       int(69),
                       int(70)]#,
                       #int(1),      # Speed
                       #int(200),    # Brightness
                       #int(116),    # hPal
                       #int(0),      # hPalMode
                       #int(1)]      # hRGBMode

        # assign global setParameters
        self.global_parameter = array
        # self.global_labels = labels
        self.test_list = [64 for i in range(3000)]

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

        # try to establish connection to arduino
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 230400)
            logging.info('Connection to Arduino established')
            logging.info(self.arduino)
        except IOError:
            try:
                self.arduino = serial.Serial('/dev/ttyACM1', 230400)
                logging.info('Connection to Arduino established')
                logging.info(self.arduino)
            except IOError:
                self.debug = True
                logging.warning('No Connection to Arduino established, entering DEBUG mode')

        # setup empty world
        self.cubeworld = np.zeros([3, 10, 10, 10])
        self.channelworld = np.zeros([4, 3, 10, 10, 10])

        # initialise channels
        self.channels = []
        self.channels.append(class_channel(1))
        self.channels.append(class_channel(2))
        self.channels.append(class_channel(3))
        self.channels.append(class_channel(4))

        logging.warning('Initialisation complete')
        print('init renderer')

    def run(self):
        """generates a frame and sends the package when cube is turned on"""
        # check wether 'running' flag is set
        if self.global_parameter[0] == 1:
            self.generate_frame()
            self.send_frame()
            self.framecounter += 1
        else:
            pass

    def send_frame(self):
        """
        Function to convert world to voxel format,
        and send it through serial interface to the
        Arduino
        """

        package = bytearray(self.header + self.get_cubedata())
        self.arduino.write(package)

        # if not self.debug:
        #     self.arduino.write(bytearray(package))
        #
        # else:
        #     logging.info('Frame '+str(self.framecounter))
        #     logging.info(package)

    def generate_frame(self):
        """
        Calculates a new frame according to the
        entries in the global parameter variable

        writes the result into self.cubeworld
        """
        # perform calculation of frames
        # in order to pass the right midivalues/parameters
        index_settings = 20     # information about choice of generators, ...
        index_parameters = 40   # parameter like brightness, generator settings, ...

        index_label = 0

        for i in range(4):      # loop through channels
            channel = self.channels[i]
            # check whether cannel is active, otherwise overrides channel world
            # with zeros
            if int(self.global_parameter[index_parameters]) == 1:
                # check for changes
                if channel.get_settings() != self.global_parameter[index_settings:index_settings+5]:
                    # pass channel settings
                    channel.set_settings(self.global_parameter[index_settings:index_settings+5])

                # calculate frame
                new_world = channel.render_frame(self.framecounter, self.global_parameter[index_parameters:index_parameters+30])

				# get current values
                # print(channel.get_labels())

            else:
                new_world = np.zeros([3, 10, 10, 10])

            # apply fade
            self.channelworld[i, :, :, :] = new_world + self.global_parameter[index_parameters+2]*\
                                             self.channelworld[i, :, :, :]
            # increase index
            index_settings += 5
            index_parameters += 30
            index_label += 16

        # calculate brightness for channels
        # we have the problem, that we want the channels to add
        # up, but only have a limited brightness - so things can
        # produce an 'overexposure'
        # as a workaround, i'm inserting a global parameter to control
        # the maximum brightness of each individual channel, so addings
        # things can actually incease the brightness a bit more

        channel_brightness = [np.clip(self.global_parameter[41], 0, self.global_parameter[3]),
                              np.clip(self.global_parameter[71], 0, self.global_parameter[3]),
                              np.clip(self.global_parameter[101], 0, self.global_parameter[3]),
                              np.clip(self.global_parameter[131], 0, self.global_parameter[3])]

#                                     channel_brightness = [i*1/255.0 for i in channel_brightness]

        # copy channels together
        self.cubeworld = self.global_parameter[2] * self.cubeworld +\
                         channel_brightness[0] * self.channelworld[0, :, :, :] +\
                         channel_brightness[1] * self.channelworld[1, :, :, :] +\
                         channel_brightness[2] * self.channelworld[2, :, :, :] +\
                         channel_brightness[3] * self.channelworld[3, :, :, :]

        # adjust global brightness
        self.cubeworld *= self.global_parameter[1]
        #print(self.framecounter)

    def get_cubedata(self):
        """get vox format from the internal stored world"""
        list1 = world2vox(np.clip(self.cubeworld[0, :, :, :], 0, 1))
        list2 = world2vox(np.clip(self.cubeworld[1, :, :, :], 0, 1))
        list3 = world2vox(np.clip(self.cubeworld[2, :, :, :], 0, 1))

        #print('')
        #print(self.cubeworld[:, 0, 0, 0])
        #print(list1[:3])

        # stack this lists for each color, so that we have RGB ordering for
        # each LED
        liste = list(np.stack((list1, list2, list3)).flatten('F'))
        #print(liste[:10])
        return liste
