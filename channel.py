import numpy as np
import logging
# from speed_decorator import speed_decorator
from collection import generators, effects


class class_channel():
    '''
    Class for a channel
    '''
    def __init__(self):
        '''
        initialises a channel
        '''
        self.generator = generators[0]()
        self.effect_1 = effects[0]()
        self.effect_2 = effects[0]()
        self.effect_3 = effects[0]()
        logging.info('Channel initialised')

    def set_settings(self, settings):
        '''
        sets the settings of a channel
        '''
        self.generator = generators[int(settings[0])]()
        self.effect_1 = effects[int(settings[1])]()
        self.effect_2 = effects[int(settings[2])]()
        self.effect_3 = effects[int(settings[3])]()

    def render_frame(self, framecounter, parameters):
        '''
        renders frame
        *args contains the all the parameters of a channel
        '''
        # settings parameters
        self.generator.control(parameters[5:10])
        self.effect_1.control(parameters[10:15])
        self.effect_2.control(parameters[15:20])
        self.effect_3.control(parameters[20:25])

        # calculate everything
        if framecounter % int(parameters[3]*40+1) == 0:
            world = self.generator.generate(framecounter)
            world = self.effect_1.generate(framecounter, world)
            world = self.effect_2.generate(framecounter, world)
            world = self.effect_3.generate(framecounter, world)

        else:
            world = np.zeros([3, 10, 10, 10])

        return world
