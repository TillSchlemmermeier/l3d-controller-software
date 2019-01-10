
import numpy as np
import logging
import serial
from world2vox_fortran import world2vox_f as world2vox
from global_parameter_module import global_parameter
from channel import class_channel

class rendering_engine:
    '''
    L3D Cube 3.0

    class for the rendering engine

    assuming a global variable called
    'global_parameter':
    - numpy array with size of 255
    - entries ordered as described in
      readme

    '''
    def __init__(self, log=False):

        # initialise variables
        self.framecounter = 0
        self.logging = log
        self.debug = False
        self.header = [int(66),
                       int(69),
                       int(69),
                       int(70),
                       int(1),      # Speed
                       int(200),    # Brightness
                       int(116),    # hPal
                       int(0),      # hPalMode
                       int(1),      # hRGBMode
                       ]

        # take care of logging
        if self.logging:
            logging.basicConfig(filename='log_rendering_enginge.log',
                                level=logging.DEBUG,
                                format='%(asctime)s %(message)s')
#                                datefmt='%m/%d/%Y %I:%M:%S %p')
        else:
            logging.basicConfig(filename='log_rendering_enginge.log',
                                level=logging.WARNING,
                                format="%(asctime)s %(message)s")
#                                datefmt='%m/%d/%Y %I:%M:%S %p')

        logging.info('Variables initialised')

        # try to establish connection to arduino
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 230400)
            logging.info('Connection to Arduino established')
            logging.info(self.arduino)
        # except IOError:
        #    self.arduino = serial.Serial('/dev/ttyACM1', 230400)
        #    logging.info('Connection to Arduino established')
        #    logging.info(self.arduino)
        except:
            self.debug = True
            logging.warning('No Connection to Arduino established, entering DEBUG mode')

        # setup empty world
        self.cubeworld = np.zeros([3, 10, 10, 10])
        self.channelworld = np.zeros([4, 3, 10, 10, 10])

        # initialise channels
        self.channels = []
        self.channels.append(class_channel())
        self.channels.append(class_channel())
        self.channels.append(class_channel())
        self.channels.append(class_channel())

        logging.warning('Initialisation complete')

    def run(self):
        # check wether 'running' flag is set
        if global_parameter[0] == 1:
            self.generate_frame()
            self.send_frame()
            # increase framecounter
            self.framecounter += 1
            # some test to emulate output to arduino
            print('Frame', self.framecounter)
        else:
            print('Frame', self.framecounter)

    def send_frame(self):
        '''
        Function to convert world to voxel format,
        and send it through serial interface to the
        Arduino
        '''
        if not self.debug:
            # assemble list
            package = self.header + self.get_cubedata()
            # send package
            self.arduino.write(bytearray(package))
        else:
            # logging.info(self.cubeworld)
            logging.info('Frame '+str(self.framecounter))

    def test(self):
        '''
        test generator
        '''
        world = np.zeros([3, 10, 10, 10])
        world[0, :, :, :] = 0.5

        return world

    def generate_frame(self):
        '''
        Calculates a new frame according to the
        entries in the global parameter variable

        writes the result into self.cubeworld
        '''
        # perform calculation of frames
        # in order to pass the right midivalues/parameters
        index_settings = 20     # information about choice of generators, ...
        index_parameters = 40   # parameter like brightness, generator settings, ...

        for i in range(4):
            channel = self.channels[i]
            # check whether cannel is active, otherwise overrides channel world
            # with zeros
            if int(global_parameter[index_parameters]) == 1:
                # pass channel settings
                channel.set_settings(global_parameter[index_settings:index_settings+5])
                # calculate frame
                new_world = channel.render_frame(self.framecounter, global_parameter[index_parameters:index_parameters+30])
            else:
                new_world = np.zeros([3, 10, 10, 10])

            # apply fade
            self.channelworld[i, :, :, :] = new_world + global_parameter[index_parameters+2]*\
                                            self.channelworld[i, :, :, :]
            # increase index
            index_settings += 5
            index_parameters += 30

        # calculate brightness for channels
        # we have the problem, that we want the channels to add
        # up, but only have a limited brightness - so things can
        # produce an 'overexposure'
        # as a workaround, i'm inserting a global parameter to control
        # the maximum brightness of each individual channel, so addings
        # things can actually incease the brightness a bit more
        channel_brightness = [np.clip(global_parameter[41], 0, global_parameter[3]),
                              np.clip(global_parameter[71], 0, global_parameter[3]),
                              np.clip(global_parameter[101], 0, global_parameter[3]),
                              np.clip(global_parameter[131], 0, global_parameter[3])]

        channel_brightness = [i*1/255.0 for i in channel_brightness]

        # copy channels together
        self.cubeworld = global_parameter[2] * self.cubeworld +\
                         channel_brightness[0] * self.channelworld[0, :, :, :] +\
                         channel_brightness[1] * self.channelworld[1, :, :, :] +\
                         channel_brightness[2] * self.channelworld[2, :, :, :] +\
                         channel_brightness[3] * self.channelworld[3, :, :, :]

        # adjust global brightness
        self.cubeworld *= global_parameter[1]

    def get_cubedata(self):
        # get vox format from the internal stored world
        # get each color
        list1 = world2vox(self.cubeworld[0, :, :, :])
        list2 = world2vox(self.cubeworld[1, :, :, :])
        list3 = world2vox(self.cubeworld[2, :, :, :])

        # stack this lists for each color, so that we have RGB ordering for
        # each LED
        liste = list(np.stack((list1, list2, list3)).flatten('F'))

        return liste
