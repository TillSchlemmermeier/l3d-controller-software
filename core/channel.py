from element_registry import new_element
from effects.e_color_manager import e_color_manager

class class_channel:
    '''Class for a channel'''
    def __init__(self, id = 0):
        '''initialises a channel'''
        self.id = id
        self.generator = None
        self.effects = []
        self.color_effect = e_color_manager()
        
    def update_channel(self, channelstate):
        # check if generator values need to be updated
        if channelstate[9]['update']:
            # check if generator changed
            if channelstate[9]['name'] != self.generator.__class__.__name__:
                # if so, replace old generator with instance of the new one
                self.generator = new_element('generator', channelstate[9]['name'])

        # if effects were removed, remove them from the list
        if channelstate['numberOfEffects'] < len(self.effects):
            self.effects = self.effects[:channelstate['numberOfEffects']]
        
        # loop over the effects and check if they need to be updated
        for i in range(channelstate['numberOfEffects']):
            if channelstate[i]['update']:
                # if the effect was added, add a new instance to the list
                if i >= len(self.effects):
                    self.effects.append(new_element('effect', channelstate[i]['name']))
                # otherwise check if effect changed and if so, replace old effect with instance of the new one
                elif channelstate[i]['name'] != self.effects[i].__class__.__name__:
                    self.effects[i] = new_element('effect', channelstate[i]['name'])

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

        if 8 in channelstate:
            if channelstate[8]['update']:
                world = self.color_effect(world, channelstate[8])
                channelstate[8]['update'] = False
            else:
                world = self.color_effect(world)

        return world, channelstate if channel_updated else None
