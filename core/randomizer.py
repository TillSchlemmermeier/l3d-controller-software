import random
import threading
import time
import requests
from db_manager import DatabaseManager
from state_manager import StateManager
import json

class Randomizer:
    def __init__(self, state):
        self.db = DatabaseManager()
        self.state_manager = StateManager(state)
        self.state = state

        self.api_endpoint = "http://localhost:8000/api"
        self.url = f"{self.api_endpoint}/get-state"

        # --- Thread Management ---
        self._current_cancel_event = None
        self._current_load_thread = None
        self._thread_lock = threading.Lock()
        self.expected_number_of_channels = 0

        self.number_of_channels = 0
        self.context = [[0, 0], [0, 0], [0, 0], [0, 0]]

    def trigger(self) -> None:
        """Trigger random action based on current mode"""
        # Cancel any running slow load thread before starting a new randomization
        with self._thread_lock:
            if self._current_cancel_event:
                self._current_cancel_event.set()
                if self._current_load_thread and self._current_load_thread.is_alive():
                    print("Cancelling previous slow load task...")

        with self.state.lock:
            mode = self.state.get('random', 'global')
            self.number_of_channels = self.state['numberOfChannels']
            self.context = self.state['context']
        
        if mode == 'global':
            self._randomize_global()
        elif mode == 'all_channels':
            self._randomize_all_channels()
        elif mode == 'all_elements':
            self._randomize_all_elements()
        elif mode == 'random_channel':
            self._randomize_single_channel()
        elif mode == 'random_channel_elements':
            self._randomize_all_elements(randomize=True)
        elif mode == 'selected_channel':
            self._randomize_single_channel(selected_only=True)
        elif mode == 'selected_channel_elements':
            self._randomize_all_elements(selected_only=True)
        elif mode == 'random_element':
            self._randomize_single_element()
        elif mode == 'selected_element':
            self._randomize_single_element(True)

    def _randomize_global(self) -> None:
        """Load random global preset"""
        presets = self.db.get_preset_names('global', 'presets')
        if presets:
            preset = random.choice(presets)
            preset_data = self.db.get_preset('global', 'presets', preset['name'], False)
            # 1. Update global settings first
            self.state_manager.load_global(preset_data, False)

            # Create a unique event for THIS specific task instance
            cancel_event = threading.Event()

            def slow_load_task():
                try:
                    # Use the local 'cancel_event' instead of self._stop_slow_load_event
                    if cancel_event.is_set(): return
                    self.expected_number_of_channels = preset_data['numberOfChannels']

                    # 2. Update channels one by one with delay
                    for i in range(preset_data['numberOfChannels']):
                        if cancel_event.is_set():
                            print("Slow load aborted during channel update.")
                            return

                        self.state_manager.load_channel(i, preset_data[i])
                        with self.state.lock:
                            self.state['numberOfChannels'] = max(self.state['numberOfChannels'], i + 1)

                        requests.get(self.url)

                        # Sleep in small chunks to allow faster interruption
                        for _ in range(30):
                            if cancel_event.is_set(): return
                            time.sleep(0.1)

                    # 3. Cleanup extra channels
                    if cancel_event.is_set(): return

                    print("Starting cleanup of extra channels")
                    current_max = 8

                    for i in range(current_max, self.expected_number_of_channels - 1, -1):
                        if cancel_event.is_set():
                            print("Slow load aborted during cleanup.")
                            return

                        channel_exists = False
                        with self.state.lock:
                            if i in self.state:
                                channel_exists = True

                        if channel_exists:
                            self.state_manager.remove_channel(i)
                            requests.get(self.url)

                            for _ in range(30):
                                if cancel_event.is_set(): return
                                time.sleep(0.1)
                        else:
                            # If channel doesn't exist, continue immediately
                            pass

                    if cancel_event.is_set(): return

                    with self.state.lock:
                        self.state['midi_update'] = 1
                    requests.get(self.url)
                    print("Cleanup complete. Final numberOfChannels:", self.state['numberOfChannels'])

                except Exception as e:
                    print(f"[CORE] Error in slow load task: {e}")

            # Start the background thread
            with self._thread_lock:
                # Register the new event and thread
                self._current_cancel_event = cancel_event
                self._current_load_thread = threading.Thread(target=slow_load_task)
                self._current_load_thread.daemon = True
                self._current_load_thread.start()

    def _randomize_all_channels(self) -> None:
        """Load random channel preset for each channel"""
        presets = self.db.get_preset_names('channel', 'presets')
        if not presets:
            return

        for i in range(self.number_of_channels):
            preset = random.choice(presets)
            preset_data = self.db.get_preset('channel', 'presets', preset['name'], False)
            self.state_manager.load_channel(i, preset_data)

    def _randomize_single_channel(self, selected_only: bool = False) -> None:
        """Load random preset for random channel"""
        if selected_only:
            channel_idx = self.context[0][0]
            if channel_idx >= self.state['numberOfChannels']:
                with self.state.lock:
                    self.state['numberOfChannels'] += 1
                    channel_idx = self.state['numberOfChannels'] - 1
        else:
            channel_idx = random.randint(0, self.state['numberOfChannels'] - 1)

        presets = self.db.get_preset_names('channel', 'presets')
        if presets:
            preset = random.choice(presets)
            preset_data = self.db.get_preset('channel', 'presets', preset['name'], False)
            self.state_manager.load_channel(channel_idx, preset_data)

    def _randomize_all_elements(self, selected_only: bool = False, randomize: bool = False) -> None:
        """Load random generators/effects for all slots"""
        active_generators = self.db.get_active_elements('generator')
        active_effects = self.db.get_active_elements('effect')
        
        if not active_generators or not active_effects:
            return

        if selected_only:
            channel_idx = self.context[0][0]
            if channel_idx >= self.number_of_channels:
                return
            channels_to_randomize = [channel_idx]
        elif randomize:
            channel_idx = random.randint(0, self.number_of_channels - 1)
            channels_to_randomize = [channel_idx]
        else:
            channels_to_randomize = range(self.number_of_channels)

        # Randomize each channel
        for channel_idx in channels_to_randomize:
            # Randomize generator
            generator = random.choice(active_generators)
            generator_presets = self.db.get_preset_names('generator', generator['name'])
            if generator_presets:
                preset = random.choice(generator_presets)
                preset_data = self.db.get_preset('generator', generator['name'], preset['name'], False)
                self.state_manager.load_generator(channel_idx, preset_data)
            # Randomize effects
            channel = None
            with self.state.lock:
                channel = self.state[channel_idx]
            for effect_idx in range(channel['numberOfEffects']):
                effect = random.choice(active_effects)
                effect_presets = self.db.get_preset_names('effect', effect['name'])
                if effect_presets:
                    preset = random.choice(effect_presets)
                    preset_data = self.db.get_preset('effect', effect['name'], preset['name'], False)
                    self.state_manager.load_effect(channel_idx, effect_idx, preset_data)
            # Randomize color
            self._randomize_color(channel_idx)


    def _randomize_single_element(self, selected_only: bool = False) -> None:
        """Load random preset for random element in state"""

        elements_in_channel = []

        if not selected_only:
            # 1. Randomly select a channel
            channel_idx = random.randint(0, self.number_of_channels - 1)

            channel = None
            with self.state.lock:
                channel = self.state[channel_idx]

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

            # Add color element (index 8)
            if 8 in channel:
                elements_in_channel.append({
                    'channel': channel_idx,
                    'index': 8,
                })

            if not elements_in_channel:
                return

        else:
            # If selected_only is True, use only the currently selected element
            channel = self.context[0][0]
            element = self.context[0][1]

            if channel >= self.number_of_channels:
                return

            elements_in_channel.append({
                'channel': channel,
                'index': element
            })

        # 3. Randomly select one element from the channel
        selected_element = random.choice(elements_in_channel)

        # 4. Get new random element from database based on type
        if selected_element['index'] == 8:
            # For color element
            self._randomize_color(selected_element['channel'])
        else:
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


    def _randomize_color(self, channel_idx: int) -> None:
        """Randomize color gradient for a channel"""
        # Random gradient type
        gradient_types = ['linear', 'radial']
        gradient_type = random.choice(gradient_types)

        gradients = self.db.get_all_gradients()
        gradient_string = random.choice(gradients)['data']
        gradient = json.loads(gradient_string)

        # Random speeds (-100 to 100)
        speed = random.randint(0, 100)
        rotate_speed_y = random.randint(-100, 100)
        rotate_speed_z = random.randint(-100, 100)

        # Random section (0-100)
        section_start = random.randint(0, 80)
        section_width = random.randint(20, 100 - section_start)

        # Sound to Light Options
        s2l_options = ['startVal', 'endVal', 'startSat', 'endSat', 'regionWidth', 'regionStart', 'speed', 'rotateY', 'rotateZ']
        # Triangular distribution: Low = 0, High = 9 (exclusive), Mode (peak) = 1
        k = int(random.triangular(0, 9, 1))
        s2l = random.sample(s2l_options, k)

        color_data = {
            'gradient': gradient,
            'gradientType': gradient_type,
            'speed': speed,
            'sectionStart': section_start,
            'sectionWidth': section_width,
            'rotateSpeedY': rotate_speed_y,
            'rotateSpeedZ': rotate_speed_z,
            'soundToLightOptions': s2l,
            'update': True
        }

        # Update via state manager
        self.state_manager.update_color_manager(channel_idx, color_data)