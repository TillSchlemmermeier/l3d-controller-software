import random
from typing import List, Dict, Optional
from db_manager import DatabaseManager
from state_manager import StateManager


class Randomizer:
    def __init__(self):
        self.db = DatabaseManager()
        self.state_manager = StateManager()
        self.state = self.state_manager.state

    def trigger(self) -> None:
        """Trigger random action based on current mode"""
        mode = self.state.get('random', 'global')
        
        if mode == 'global':
            self._randomize_global()
        elif mode == 'all_channels':
            self._randomize_all_channels()
        elif mode == 'single_channel':
            self._randomize_single_channel()
        elif mode == 'all_elements':
            self._randomize_all_elements()
        elif mode == 'single_element':
            self._randomize_single_element()

    def _randomize_global(self) -> None:
        """Load random global preset"""
        presets = self.db.get_preset_names('global', 'presets')
        if presets:
            preset = random.choice(presets)
            preset_data = self.db.get_preset('global', 'presets', preset['name'], False)
            self.state_manager.load_global(preset_data)

    def _randomize_all_channels(self) -> None:
        """Load random channel preset for each channel"""
        presets = self.db.get_preset_names('channel', 'presets')
        if not presets:
            return
            
        for i in range(self.state['numberOfChannels']):
            preset = random.choice(presets)
            preset_data = self.db.get_preset('channel', 'presets', preset['name'], False)
            self.state_manager.load_channel(i, preset_data)

    def _randomize_single_channel(self) -> None:
        """Load random preset for random channel"""
        if self.state['numberOfChannels'] == 0:
            return
            
        channel_idx = random.randint(0, self.state['numberOfChannels'] - 1)
        presets = self.db.get_preset_names('channel', 'presets')
        if presets:
            preset = random.choice(presets)
            preset_data = self.db.get_preset('channel', 'presets', preset['name'], False)
            self.state_manager.load_channel(channel_idx, preset_data)

    def _randomize_all_elements(self) -> None:
        """Load random generators/effects for all slots"""
        active_generators = self.db.get_active_elements('generator')
        active_effects = self.db.get_active_elements('effect')
        
        if not active_generators or not active_effects:
            return

        # Randomize each channel
        for channel_idx in range(self.state['numberOfChannels']):
            # Randomize generator
            generator = random.choice(active_generators)
            generator_presets = self.db.get_preset_names('generator', generator['name'])
            if generator_presets:
                preset = random.choice(generator_presets)
                preset_data = self.db.get_preset('generator', generator['name'], preset['name'], False)
                self.state_manager.load_generator(channel_idx, preset_data)
            # Randomize effects
            channel = self.state[channel_idx]
            for effect_idx in range(channel['numberOfEffects']):
                effect = random.choice(active_effects)
                effect_presets = self.db.get_preset_names('effect', effect['name'])
                if effect_presets:
                    preset = random.choice(effect_presets)
                    preset_data = self.db.get_preset('effect', effect['name'], preset['name'], False)
                    self.state_manager.load_effect(channel_idx, effect_idx, preset_data)

    def _randomize_single_element(self) -> None:
        """Load random preset for random element in state"""
        # 1. Randomly select a channel
        channel_idx = random.randint(0, self.state['numberOfChannels'] - 1)
        channel = self.state[channel_idx]

        # 2. Build list of possible elements in this channel
        elements_in_channel = []

        # Add generator (index 9)
        if 9 in channel:
            elements_in_channel.append({
                'channel': channel_idx,
                'index': 9
            })

        # Add effects (0 to numberOfEffects-1)
        for effect_idx in range(channel['numberOfEffects']):
            if effect_idx in channel:
                elements_in_channel.append({
                    'channel': channel_idx,
                    'index': effect_idx
                })

        if not elements_in_channel:
            return

        # 3. Randomly select one element from the channel
        selected_element = random.choice(elements_in_channel)

        # 4. Get new random element from database based on type
        if selected_element['index'] == 9:
            # For generator
            active_generators = self.db.get_active_elements('generator')
            if not active_generators:
                return
            new_element = random.choice(active_generators)
            element_type = 'generator'
        else:
            # For effect
            active_effects = self.db.get_active_elements('effect')
            if not active_effects:
                return
            new_element = random.choice(active_effects)
            element_type = 'effect'

        # 5. Get random preset for the new element
        presets = self.db.get_preset_names(element_type, new_element['name'])
        if not presets:
            return

        preset = random.choice(presets)
        preset_data = self.db.get_preset(element_type, new_element['name'], preset['name'], False)

        if not preset_data:
            return

        # 6. Load the preset
        if element_type == 'generator':
            self.state_manager.load_generator(selected_element['channel'], preset_data)
        else:
            self.state_manager.load_effect(selected_element['channel'], selected_element['index'], preset_data)