import random
import threading
import time
import queue
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
        self.current_cancel_event = None
        self.current_load_thread = None
        self.thread_lock = threading.Lock()
        self.expected_number_of_channels = 0

        self.number_of_channels = 0
        self.context = [[0, 0], [0, 0], [0, 0], [0, 0]]

    def run_autopilot_loop(self, state, randomizer_queue):
        starttime = time.time()

        autopilot_on = False
        autopilot_interval = 3
        last_state_check = 0

        while True:
            # Check state every 0.5 second
            current_time = time.time()
            if current_time - last_state_check > 0.5:
                with state.lock:
                    autopilot_on = state['autopilot']
                    autopilot_interval = state['autopilot_time']
                last_state_check = current_time

            # Wait up to 0.1 seconds for a manual trigger message
            try:
                message = randomizer_queue.get(timeout=0.1)
                if isinstance(message, int):
                    self.randomize_color(message)
                else:
                    self.trigger(message)
            except queue.Empty:
                pass  # No message, proceed

            # Autopilot logic (uses cached values)
            if autopilot_on:
                if current_time - starttime > 2 + autopilot_interval:
                    self.trigger()
                    starttime = current_time
            else:
                starttime = current_time

    def trigger(self, mode=None) -> None:
        """Trigger random action based on current mode"""
        # Cancel any running slow load thread before starting a new randomization
        with self.thread_lock:
            if self.current_cancel_event:
                self.current_cancel_event.set()
                if self.current_load_thread and self.current_load_thread.is_alive():
                    print("Cancelling previous slow load task...")

        with self.state.lock:
            if mode is None:
                mode = self.state.get('random', 'global')
            self.number_of_channels = self.state['numberOfChannels']
            self.context = self.state['context']
        
        if mode == 'global':
            self.randomize_global()

        elif mode == 'all_channels':
            for i in range(self.number_of_channels):
                self.randomize_single_channel(i)

        elif mode == 'all_elements':
            channels_to_randomize = range(self.number_of_channels)
            self.randomize_all_elements(channels_to_randomize)

        elif mode == 'random_channel':
            channel_idx = random.randint(0, self.state['numberOfChannels'] - 1)
            self.randomize_single_channel(channel_idx)

        elif mode == 'random_channel_elements':
            channel_idx = random.randint(0, self.number_of_channels - 1)
            self.randomize_all_elements([channel_idx])

        elif mode == 'selected_channel':
            self.randomize_single_channel(self.context[0][0])

        elif mode == 'selected_channel_elements':
            channel_idx = self.context[0][0]
            if channel_idx >= self.number_of_channels:
                return
            self.randomize_all_elements([channel_idx])

        elif mode == 'random_element':
            channel_idx = random.randint(0, self.number_of_channels - 1)

            with self.state.lock:
                channel = self.state[channel_idx]
            # get all keys that are integers (8: colors, 9: generator, 0..n: effects)
            available_indices = [k for k in channel if isinstance(k, int)]

            element_idx = random.choice(available_indices)
            self.randomize_single_element(channel_idx, element_idx)

        elif mode == 'selected_element':
            channel_idx = self.context[0][0]
            element_idx = self.context[0][1]
            self.randomize_single_element(channel_idx, element_idx)

        # wait 50 ms to make sure rendering engine has processed the state change
        time.sleep(0.05)
        requests.get(self.url)

    def randomize_global(self) -> None:
        """Load random global preset"""
        presets = self.db.get_preset_names('global', 'presets')
        if presets:
            preset = random.choice(presets)
            preset_data = self.db.get_preset('global', 'presets', preset['name'], False)

            # Update global settings first, don't load the preset fully yet
            self.state_manager.load_global(preset_data, False)

            # Create a unique event for THIS specific task instance
            cancel_event = threading.Event()

            def slow_load_task():
                try:
                    # Use the local 'cancel_event' instead of self.stop_slow_load_event
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
            with self.thread_lock:
                # Register the new event and thread
                self.current_cancel_event = cancel_event
                self.current_load_thread = threading.Thread(target=slow_load_task)
                self.current_load_thread.daemon = True
                self.current_load_thread.start()

    def randomize_single_channel(self, channel_idx: int) -> None:
        """Load random preset for random channel"""
        if channel_idx >= self.state['numberOfChannels']:
            with self.state.lock:
                self.state['numberOfChannels'] += 1
                channel_idx = self.state['numberOfChannels'] - 1

        presets = self.db.get_preset_names('channel', 'presets')
        preset = random.choice(presets)
        preset_data = self.db.get_preset('channel', 'presets', preset['name'], False)
        self.state_manager.load_channel(channel_idx, preset_data)

    def randomize_all_elements(self, channels_to_randomize: list) -> None:
        """Load random generators/effects for all slots"""
        for channel_idx in channels_to_randomize:
            with self.state.lock:
                channel = self.state[channel_idx]
            # get all keys that are integers (8: colors, 9: generator, 0..n: effects)
            elements = [k for k in channel if isinstance(k, int)]
            if 8 not in elements:
                elements.append(8)

            for element in elements:
                self.randomize_single_element(channel_idx, element)

    def randomize_single_element(self, channel_idx: int, element_idx: int) -> None:
        """Load random preset for a specific or random element"""
        if element_idx == 8:
            self.randomize_color(channel_idx)
            return

        presets_available = [
        "g_bouncer",
        "g_circles",
        "g_corner",
        "g_corner_grow",
        "g_cube",
        "g_cube_edges",
        "g_cut",
        "g_drop",
        "g_edge_lines",
        "g_falling",
        "g_flash",
        "g_fountaine",
        "g_planes",
        "g_torus",
        "e_black_color_white",
        "e_break_fade",
        "e_bright_mod",
        "e_bright_osci",
        "e_brightness_wave",
        "e_compressor",
        "e_fade",
        "e_invert",
        "e_mean",
        "e_mirror",
        "e_random_brightness",
        "e_randomizer",
        "e_rare_strobo",
        "e_slicer",
        "e_squared"
        "e_strobe",
        ]

        element_type = 'generator' if element_idx == 9 else 'effect'
        active_elements = self.db.get_active_elements(element_type)

        new_element = random.choice(active_elements)
        if new_element['name'] in presets_available:
            presets = self.db.get_preset_names(element_type, new_element['name'])

            preset = random.choice(presets)
            preset_data = self.db.get_preset(element_type, new_element['name'], preset['name'], False)

        else:
            preset_data = self.db.get_preset(element_type, new_element['name'], 'basic', False)
            params = preset_data['params']
            num_params = len(params) // 4
            for i in range(num_params):
                params[i * 4 + 3] = random.random()

        if element_type == 'generator':
            self.state_manager.load_generator(channel_idx, preset_data)
        else:
            self.state_manager.load_effect(channel_idx, element_idx, preset_data)

    def randomize_color(self, channel_idx: int) -> None:
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
        requests.get(self.url)