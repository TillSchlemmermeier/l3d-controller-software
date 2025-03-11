import logging
from UltraDict import UltraDict

file = open("generators.dat", "r")
generatorFile = file.readlines()
for generator in generatorFile:
    exec('from generators.' +str(generator).replace('\n','') + ' import *')

file = open("effects.dat", "r")
effectsFile = file.readlines()
for effect in effectsFile:
    exec('from effects.' + str(effect).replace('\n','') + ' import *')

class class_channel:
    '''
    Class for a channel
    '''
    def __init__(self, id = 0):
        '''
        initialises a channel
        '''
        self.id = id
        self.generator = None
        self.effects = []
        self.state = UltraDict(name='state')

        logging.info('Channel '+str(self.id)+' initialised')

    def update_channel(self, channelstate):
        # check if generator values need to be updated
        print('update channel', channelstate, self.id)
        if channelstate['generator']['update'] == True:
            # check if generator changed
            if channelstate['generator']['name'] != self.generator.__class__.__name__:
                print('update generator')
                # if so, replace old generator with instance of the new one
                exec('self.generator = ' + channelstate['generator']['name'] + '()')

            # update the generator parameters in the state with current values, leave the MIDI values
            generator = channelstate['generator']
            # check if a preset was loaded and if not, initialise the params array with zeros
            if not generator['params']:
                generator['params'] = [0 for _ in range(4 * len(self.generator.return_state()))]

            generator_state = self.generator.return_state()
            for i in range(len(generator_state)):
                generator['params'][4*i:4*i+3] = generator_state[i][:3]
            generator['update'] = 0

        # if effects were removed, remove them from the list
        if len(channelstate['effects']) < len(self.effects):
            self.effects = self.effects[:len(channelstate['effects'])]
        
        # loop over the effects and check if they need to be updated
        for i in range(len(channelstate['effects'])):
            if channelstate['effects'][i]['update'] == 1:
                # if the effect was added, add a new instance to the list
                if i >= len(self.effects):
                    exec('self.effects.append(' + channelstate['effects'][i]['name'] + '())')
                # otherwise check if effect changed and if so, replace old effect with instance of the new one
                elif channelstate['effects'][i]['name'] != self.effects[i].__class__.__name__:
                    exec('self.effects[i] = ' + channelstate['effects'][i]['name'] + '()')

                # update the effect parameters in the state with current values, leave the MIDI values
                effect = channelstate['effects'][i]
                # check if a preset was loaded and if not, initialise the params array with zeros
                if not effect['params']:
                    effect['params'] = [0 for _ in range(4 * len(self.effects[i].return_state()))]
                effect_state = self.effects[i].return_state()
                for k in range(len(effect_state)):
                    effect['params'][4*k:4*k+3] = effect_state[k][:3]
                effect['update'] = 0
        print('update channel completed', channelstate)
        return channelstate

    def render_frame(self, framecounter, channelstate):
        '''
        renders frame
        '''
        # create world from generator
        world = self.generator(channelstate['generator']['params'][3::4])
        # apply the effects to the world, using the midi values the effect parameters
        for i in range(len(self.effects)):
            if channelstate['effects'][i]['IO'] == 1:
                world = self.effects[i](world, channelstate['effects'][i]['params'][3::4])

        return world
