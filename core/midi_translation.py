from copy import deepcopy
import numpy as np
import requests
from UltraDict import UltraDict
from threading import Timer

class class_midi_translation:

    # tolerance for soft-takeover, ~2 steps of the 0.01 value grid
    PICKUP_EPS = 0.02

    def __init__(self, state):
        # self.state = UltraDict(name='state')
        self.state = state
        self.slider_values = [0, 0, 0, 0]
        self.knob_values = [0, 0, 0, 0]
        # soft-takeover ("pickup") bookkeeping, keyed by physical control
        self.pickup_prev = {}   # -> last raw fader reading (0..1)
        self.pickup_owned = {}  # -> last value we wrote, while we own the control
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
        
    def caught(self, key, target, incoming):
        """Soft-takeover ("pickup") for non-motorized faders/knobs.

        Returns True if `incoming` may drive `target` without a jump. We keep
        control while the stored value still matches what we last wrote (the
        fader then tracks 1:1). If anything else moved it — channel reorder,
        context switch, autopilot, preset — the match breaks and we re-acquire
        only once the fader crosses or reaches the value."""
        prev = self.pickup_prev.get(key)
        owned = self.pickup_owned.get(key)
        self.pickup_prev[key] = incoming
        if owned is not None and abs(target - owned) <= self.PICKUP_EPS:
            self.pickup_owned[key] = incoming      # still in sync → keep control
            return True
        if abs(incoming - target) <= self.PICKUP_EPS or (
                prev is not None and (prev - target) * (incoming - target) <= 0):
            self.pickup_owned[key] = incoming      # crossed/reached → acquire
            return True
        return False                                # still hunting → ignore

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
                            params = this_channel[index]['params']
                            slot = midi_index * 4 + 3
                            if not self.caught((context_index, midi_index), params[slot], midi_value):
                                return
                            params[slot] = midi_value
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
                if not self.caught((key, midi_index), channel[key], midi_value):
                    return
                channel[key] = midi_value
                self.state[midi_index] = channel
                self.trigger_update(f"{self.api_endpoint}/update_key/{key}?channel={midi_index}")

            except:
                pass

        if midi_index == 8:
            if not self.caught((key, 8), self.state[key], midi_value):
                return
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
