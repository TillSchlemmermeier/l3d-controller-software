import numpy as np
import logging
from collection import generators, effects


class class_channel:
    '''
    Class for a channel
    '''
    def __init__(self, id = 0):
        '''
        initialises a channel by calling g_blank
        and e_blank
        '''
        self.id = id
        self.generator = generators[0]()
        self.effect_1 = effects[0]()
        self.effect_2 = effects[0]()
        self.effect_3 = effects[0]()
        logging.info('Channel '+str(self.id)+' initialised')

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
        '''
        world = self.generator(parameters[5:10])

        world = self.effect_1(world, parameters[10:15])
        world = self.effect_2(world, parameters[15:20])
        world = self.effect_3(world, parameters[20:25])
        # print(world)

        return world
