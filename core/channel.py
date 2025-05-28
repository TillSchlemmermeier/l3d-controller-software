from UltraDict import UltraDict
from db_manager import DatabaseManager

db = DatabaseManager()

generators = [gen['name'] for gen in db.get_active_elements('generator')]
effects = [eff['name'] for eff in db.get_active_elements('effect')]

for generator in generators:
    exec(f'from generators.{generator} import *')
for effect in effects:
    exec(f'from effects.{effect} import *')


class class_channel:
    '''Class for a channel'''
    def __init__(self, id = 0):
        '''initialises a channel'''
        self.id = id
        self.generator = None
        self.effects = []
        self.state = UltraDict(name='state')

        print('Channel '+str(self.id)+' initialised')
        
    def update_channel(self, channelstate):
        # check if generator values need to be updated
        print('update channel', channelstate, self.id)
        if channelstate[9]['update']:
            # check if generator changed
            if channelstate[9]['name'] != self.generator.__class__.__name__:
                print('update generator')
                # if so, replace old generator with instance of the new one
                exec('self.generator = ' + channelstate[9]['name'] + '()')

        # if effects were removed, remove them from the list
        if channelstate['numberOfEffects'] < len(self.effects):
            self.effects = self.effects[:channelstate['numberOfEffects']]
        
        # loop over the effects and check if they need to be updated
        for i in range(channelstate['numberOfEffects']):
            if channelstate[i]['update']:
                # if the effect was added, add a new instance to the list
                if i >= len(self.effects):
                    exec('self.effects.append(' + channelstate[i]['name'] + '())')
                # otherwise check if effect changed and if so, replace old effect with instance of the new one
                elif channelstate[i]['name'] != self.effects[i].__class__.__name__:
                    exec('self.effects[i] = ' + channelstate[i]['name'] + '()')

        print('update channel completed', channelstate)
        return channelstate

    def render_frame(self, channelstate):
        channel_updated = False

        # create world from generator
        world = self.generator(channelstate[9]['params'][3::4])

        # Update generator state values if needed
        if channelstate[9]['update']:
            generator_state = self.generator.return_state()
            for i in range(len(generator_state)):
                channelstate[9]['params'][4*i:4*i+3] = generator_state[i][:3]
            channelstate[9]['update'] = False
            channel_updated = True

        # apply the effects to the world, using the midi values
        for i in range(len(self.effects)):
            if channelstate[i]['IO'] == True:
                world = self.effects[i](world, channelstate[i]['params'][3::4])

                # Update effect state values if needed
                if channelstate[i]['update']:
                    effect_state = self.effects[i].return_state()
                    for k in range(len(effect_state)):
                        channelstate[i]['params'][4*k:4*k+3] = effect_state[k][:3]
                    channelstate[i]['update'] = False
                    channel_updated = True

        return world, channelstate if channel_updated else None
