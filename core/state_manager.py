from UltraDict import UltraDict
from copy import deepcopy

class StateManager:
    def __init__(self):
        self.state = UltraDict(name='state')

    def update_channel(self, channel_key):
        """Set update flags for channel and its components"""
        with self.state.lock:
            channel = self.state[channel_key]
            channel['update'] = 1
            if channel_key != 9:
                channel[9]['update'] = 1
            for i in range(channel['numberOfEffects']):
                channel[i]['update'] = 1
            self.state[channel_key] = channel

    def load_generator(self, channel: int, preset_data: dict, this_channel: dict = None):
        """Load a generator preset into a channel"""
        with self.state.lock:
            if this_channel is None:
                this_channel = self.state[channel]
            
            this_channel['update'] = 1
            this_channel[9] = preset_data
            this_channel[9]['update'] = 1
            
            if channel == self.state['numberOfChannels']:
                self.state['numberOfChannels'] += 1
            
            self.state[channel] = this_channel

    def load_effect(self, channel: int, effect_index: int, preset_data: dict):
        """Load an effect preset into a channel"""
        with self.state.lock:
            this_channel = self.state[channel]
            this_channel['update'] = 1
            this_channel[effect_index] = preset_data
            this_channel[effect_index]['update'] = 1
            
            if effect_index >= this_channel['numberOfEffects']:
                this_channel['numberOfEffects'] += 1
            
            self.state[channel] = this_channel

    def load_channel(self, channel: int, preset_data: dict):
        """Load a channel preset"""
        with self.state.lock:
            self.state[channel] = preset_data
            if channel == self.state['numberOfChannels']:
                self.state['numberOfChannels'] += 1
                self.state[channel]['IO'] = 0
            self.update_channel(channel)
            # update the values of the midi controller slider
            self.state['midi_update'] = 1

    def load_global(self, preset_data: dict):
        """Load a global preset"""
        with self.state.lock:
            for key, value in preset_data.items():
                self.state[key] = value

            for i in range(preset_data['numberOfChannels']):
                self.update_channel(i)
            self.update_channel(9)

            # update the values of the midi controller slider
            self.state['midi_update'] = 1

    def remove_channel(self, channel_index: int) -> bool:
        """Remove a channel and shift others up"""
        with self.state.lock:
            # Move all channels down
            for i in range(channel_index, self.state['numberOfChannels'] - 1):
                self.state[i] = deepcopy(self.state[i + 1])
                self.update_channel(i)
            
            # Clean up the last channel
            last_channel_index = self.state['numberOfChannels'] - 1
            if last_channel_index in self.state:
                del self.state[last_channel_index]
            
            self.state['numberOfChannels'] -= 1
            self.state['midi_update'] = 1

    def remove_effect(self, channel_index: int, effect_index: int):
        """Remove an effect from a channel"""
        with self.state.lock:
            channel = self.state[channel_index]
            num_effects = channel['numberOfEffects']
            
            del channel[effect_index]
            # Shift remaining effects down
            for i in range(effect_index, num_effects - 1):
                channel[i] = deepcopy(channel[i + 1])

            if num_effects - 1 in channel:
                del channel[num_effects - 1]
            channel['numberOfEffects'] -= 1
            
            self.state[channel_index] = channel
            self.update_channel(channel_index)

    def copy_channel(self, source_channel: int):
        """Copy a channel to a new slot"""
        with self.state.lock:
            new_channel_key = self.state['numberOfChannels']
            new_channel = deepcopy(self.state[source_channel])
            new_channel['IO'] = 0
            self.state[new_channel_key] = new_channel
            self.update_channel(new_channel_key)
            self.state['numberOfChannels'] += 1
            self.state['midi_update'] = 1

    def move_channel(self, from_index: int, to_index: int):
        """Move a channel to a new position"""
        with self.state.lock:
            temp_channel = deepcopy(self.state[from_index])

            if from_index < to_index:
                for i in range(from_index, to_index):
                    self.state[i] = deepcopy(self.state[i + 1])
            else:
                for i in range(from_index, to_index, -1):
                    self.state[i] = deepcopy(self.state[i - 1])

            self.state[to_index] = temp_channel
            
            for i in range(min(from_index, to_index), max(from_index, to_index) + 1):
                self.update_channel(i)
            self.state['midi_update'] = 1

    def move_effect(self, channel_index: int, from_index: int, to_index: int):
        """Move an effect within a channel to a new position"""
        with self.state.lock:
            channel = self.state[channel_index]
            effect = deepcopy(channel[from_index])

            # Reorder effects
            if from_index < to_index:
                # Moving down
                for i in range(from_index, to_index):
                    channel[i] = deepcopy(channel[i + 1])
            else:
                # Moving up
                for i in range(from_index, to_index, -1):
                    channel[i] = deepcopy(channel[i - 1])
            
            # Place effect at new position
            channel[to_index] = effect

            # Update affected effects
            for i in range(min(from_index, to_index), max(from_index, to_index) + 1):
                channel[i]['update'] = 1
            channel['update'] = 1
            
            self.state[channel_index] = channel

    def copy_effect(self, from_channel: int, from_effect_index: int, to_channel: int, to_effect_index: int):
        """Copy an effect from one channel to another"""
        with self.state.lock:
            effect = deepcopy(self.state[from_channel][from_effect_index])
            
            this_channel = self.state[to_channel]
            # Shift existing effects to make room
            for i in reversed(range(to_effect_index, this_channel['numberOfEffects'])):
                this_channel[i + 1] = this_channel[i]
            
            this_channel[to_effect_index] = effect
            this_channel['numberOfEffects'] += 1
            
            self.state[to_channel] = this_channel
            self.update_channel(to_channel)

    def toggle_effect(self, channel_index: int, effect_index: int):
        """Toggle an effect's IO state"""
        with self.state.lock:
            channel = self.state[channel_index]
            channel[effect_index]['IO'] = not channel[effect_index]['IO']
            self.state[channel_index] = channel

    def toggle_autopilot(self):
        """Toggle autopilot mode"""
        with self.state.lock:
            self.state['autopilot'] = not self.state['autopilot']

    def autopilot_mode(self):
        """Change autopilot mode"""
        modes = ['global', 'all_channels', 'single_channel', 'all_elements', 'single_element', 'selected_element']
        with self.state.lock:
            current_mode = self.state.get('random', modes[0])
            current_index = modes.index(current_mode)
            next_index = (current_index + 1) % len(modes)
            self.state['random'] = modes[next_index]

    def update_context(self, channel, index):
        with self.state.lock:
            self.state['context'] = [channel, index]
            self.state['midi_update'] = 1