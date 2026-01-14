from copy import deepcopy
import numpy as np
import requests
from UltraDict import UltraDict
from threading import Timer

class class_midi_translation:

    def __init__(self, state):
        # self.state = UltraDict(name='state')
        self.state = state
        self.slider_values = [0, 0, 0, 0]
        self.knob_values = [0, 0, 0, 0]
        self.state_a = {}
        self.state_b = {}
        self.state_diff = {}
        self.api_endpoint = "http://localhost:8000/api"
        self.session = requests.Session()

    def _send_request(self, url):
        """Helper to run in the thread"""
        try:
            self.session.get(url)
        except:
            pass

    def trigger_update(self, url):
        """
        Waits 50ms (approx 1.2 frames) before sending the update.
        This allows the rendering engine (running at 40ms/frame) to
        process the change and update the display values in the state.
        """
        Timer(0.05, self._send_request, args=[url]).start()
        
    def update_context(self, context_index, midi_index, midi_value):
        midi_index = int(midi_index)
        midi_value = round((float(midi_value) / 127.0), 2)
        try:
            with self.state.lock:  # Single lock block for all operations
                channel = self.state['context'][context_index][0] # channel is 0, 1, 2, 3, ...
                                                   # channel 9 is gloa
                index = self.state['context'][context_index][1]   # index 9 is generator, 0 first effect, ...
                
                if channel <= 9:
                    this_channel = self.state[channel]
                    if index < 10:
                        try:
                            this_channel[index]['params'][midi_index * 4 + 3] = midi_value
                            this_channel[index]['update'] = 1
                            self.state[channel] = this_channel
                        except Exception as e:
                            print(f"Error updating parameter: {e}")
                            return
        except AssertionError as e:
            print(f"UltraDict error in update_context: {e}")

        # API calls outside the lock
        if channel <= 9:
            if index < 10:
                self.trigger_update(f"{self.api_endpoint}/update_element/{channel}/{index}")
            elif index == 10:
                self.trigger_update(f"{self.api_endpoint}/update_key/{key}?channel={channel}")

        elif channel == 10:
            if index == 0:
                with self.state.lock:
                    current_values = list(self.state['s2l_values'])
                    current_thresholds = list(self.state['s2l_thresholds'])
                    if midi_index < 4:
                        current_values[midi_index] = midi_value
                        self.state['s2l_values'] = current_values
                        self.trigger_update(f"{self.api_endpoint}/update_key/s2l_values")

                    elif midi_index >= 4:
                        current_thresholds[midi_index-4] = midi_value
                        self.state['s2l_thresholds'] = current_thresholds
                        self.trigger_update(f"{self.api_endpoint}/update_key/s2l_thresholds")
                    self.state['s2l_update'] = True

            elif index == 1:
                if midi_index == 0:
                    key = 'autopilot'
                    if midi_value <= 0.5:
                        self.state[key] = False
                    elif midi_value > 0.5:
                        self.state[key] = True
                elif midi_index == 1:
                    key = 'autopilot_time'
                    self.state[key] = int(midi_value * 180)
                elif midi_index == 2:
                    key = 'random'
                    self.state[key]=['global', 'all_channels', 'all_elements', 'random_channel', 'random_channel_elements', 'selected_channel', 'selected_channel_elements', 'random_element', 'selected_element'][int(midi_value * 9)]
                elif midi_index == 3:
                    key = 's2l_normalize'
                    self.state[key] = True
                elif midi_index == 4:
                    key = 's2l_gain'
                    self.state[key] = midi_value
                elif midi_index == 5:
                    pass
                elif midi_index == 6:
                    pass

                self.trigger_update(f"{self.api_endpoint}/update_key/{key}")

    def get_context_midi_values(self):
        with self.state.lock:
            channel = self.state['context'][0][0]
            index = self.state['context'][0][1]
            if channel <= 9:
                this_channel = self.state[channel]
                if index < 10:
                    element = this_channel[index]
                    params = element['params']
                    midi_values = params[3::4]
                    return midi_values
            elif channel == 10:
                if index == 0:
                    current_values = list(self.state['s2l_values'])
                    current_thresholds = list(self.state['s2l_thresholds'])
                    s2l_values = current_values + current_thresholds
                    return s2l_values
                elif index == 1:
                    return [
                        1.0 if self.state['autopilot'] else 0.0,
                        self.state['autopilot_time'] / 180.0,
                        0.1 if self.state['random'] == 'global' else
                        0.2 if self.state['random'] == 'all_channels' else
                        0.4 if self.state['random'] == 'single_channel' else
                        0.5 if self.state['random'] == 'all_elements' else
                        0.7 if self.state['random'] == 'single_element' else
                        0.9 if self.state['random'] == 'selected_element' else 0.0,
                        0.0, #self.state['s2l_normalize']
                        self.state['s2l_gain']
                    ]

    def update_fixed(self, midi_index, key, midi_value):
        midi_index = int(midi_index)
        key = str(key)
        midi_value = round((float(midi_value) / 127.0), 2)
        if midi_index < 8:
            try:
                channel = self.state[midi_index]
                channel[key] = midi_value
                self.state[midi_index] = channel
                self.trigger_update(f"{self.api_endpoint}/update_key/{key}?channel={midi_index}")

            except:
                pass

        if midi_index == 8:
            self.state[key] = midi_value
            self.trigger_update(f"{self.api_endpoint}/update_key/{key}")
            

    def toggle_fixed(self, midi_index, key):
        midi_index = int(midi_index)
        key = str(key)
        if midi_index < 8:
            try:
                channel = self.state[midi_index]
                channel[key] = not channel[key]
                self.state[midi_index] = channel
                self.trigger_update(f"{self.api_endpoint}/update_key/{key}?channel={midi_index}")

            except:
                pass

        if midi_index == 8:
            self.state[key] = not self.state[key]
            self.trigger_update(f"{self.api_endpoint}/update_key/{key}")


    def oneshot(self, midi_index):
        print("Oneshot triggered with index:", midi_index)
        midi_index = int(midi_index)
        self.state['oneshot'] = midi_index + 2
        self.trigger_update(f"{self.api_endpoint}/update_key/oneshot")


    def save_state(self, button):
        # Create a regular dictionary from UltraDict
        state_dict = dict(self.state)
        
        # Deep copy all nested structures
        state_snapshot = {}
        for key, value in state_dict.items():
            if isinstance(value, dict):
                state_snapshot[key] = deepcopy(value)
            else:
                state_snapshot[key] = value

        if button == 'A':
            self.state_a = state_snapshot
            print("Saved state A:", self.state_a)
        elif button == 'B':
            self.state_b = state_snapshot
            print("Saved state B:", self.state_b)

        crossfade_active = self.crossfade_active()
        self.state['crossfade_active'] = crossfade_active
        self.trigger_update(f"{self.api_endpoint}/update_key/crossfade_active")

        if self.state['crossfade_active']:
            self.state_diff = self.compare_states()
            print("Differences:", self.state_diff)

        
    def crossfade_active(self):
        try:
            if self.state_a['numberOfChannels'] == self.state_b['numberOfChannels']:
                for i in range(self.state_a['numberOfChannels']):
                    # check generator names
                    if self.state_a[i][9]['name'] != self.state_b[i][9]['name']:
                        return False
                    
                    # check effect names
                    if self.state_a[i]['numberOfEffects'] == self.state_b[i]['numberOfEffects']:
                        for j in range(self.state_a[i]['numberOfEffects']):
                            if self.state_a[i][j]['name'] != self.state_b[i][j]['name']:
                                return False
                    else:
                        return False
                    
                # check global effects names
                if self.state_a[9]['numberOfEffects'] == self.state_b[9]['numberOfEffects']:
                    for k in range(self.state_a[9]['numberOfEffects']):
                        if self.state_a[9][k]['name'] != self.state_b[9][k]['name']:
                            return False
                else:
                    return False
                        
                return True
            else:
                return False

        except:        
            return False

                
        
    def compare_states(self):
        differences = {}
        
        # Compare channel parameters
        for channel_idx in range(10):  # Channels 0-9
            channel_a = self.state_a.get(channel_idx, {})
            channel_b = self.state_b.get(channel_idx, {})
            
            # Skip if channel doesn't exist in either state
            if not channel_a or not channel_b:
                continue
            
            # Compare generator first (index 9)
            generator_a = channel_a.get(9, {})
            generator_b = channel_b.get(9, {})
            
            # Always compare generator parameters
            if generator_a or generator_b:
                params_a = generator_a.get('params', [])
                params_b = generator_b.get('params', [])
                
                            # Check every 4th parameter starting at index 3
                for param_idx in range(3, len(params_a), 4):
                    if params_a[param_idx] != params_b[param_idx]:
                        key = f"{channel_idx}.9.{param_idx}"
                        differences[key] = {
                            'A': params_a[param_idx],
                            'B': params_b[param_idx]
                        }
                    
            # Compare effects in each channel
            for effect_idx in range(6):  # Up to 6 effects per channel
                effect_a = channel_a.get(effect_idx, {})
                effect_b = channel_b.get(effect_idx, {})
                
                # Skip if effect doesn't exist in either state
                if not effect_a or not effect_b:
                    continue
                    
                # Compare parameter arrays
                params_a = effect_a.get('params', [])
                params_b = effect_b.get('params', [])
                
                # Check every 4th parameter starting at index 3
                for param_idx in range(3, len(params_a), 4):
                    if params_a[param_idx] != params_b[param_idx]:
                        key = f"{channel_idx}.{effect_idx}.{param_idx}"
                        differences[key] = {
                            'A': params_a[param_idx],
                            'B': params_b[param_idx]
                        }
        
        return differences


    def crossfade(self, midi_value):
        if self.state['crossfade_active']:
            # Convert MIDI value to 0-1 range
            fade_value = float(midi_value) / 127.0
            
            # Process each differing parameter
            for key, values in self.state_diff.items():
                parts = key.split('.')
                channel_id = int(parts[0])
                element_id = int(parts[1])
                param_index = int(parts[2])
                
                # Calculate interpolated value
                value_a = values['A']
                value_b = values['B']
                current_value = round(value_a + (value_b - value_a) * fade_value, 2)
                
                try:
                    channel = self.state[channel_id]
                    # Update parameter value
                    channel[element_id]['params'][param_index] = current_value
                    # Mark both effect and channel for update
                    channel[element_id]['update'] = 1
                    channel['update'] = 1
                    # Update the state
                    self.state[channel_id] = channel
                    
                except Exception as e:
                    print(f"Error updating parameter {key}: {e}")
            
            # Notify frontend of parameter change
            self.trigger_update(f"{self.api_endpoint}/update_state")

