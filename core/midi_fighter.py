import time as time
from rtmidi.midiutil import open_midiinput,open_midioutput, open_midiport
from midi_translation import class_midi_translation
from UltraDict import UltraDict

class class_fighter:
    def __init__(self):
        """initializes the MIDI fighter"""
        self.midiin, self.portname_in = open_midiinput('Fighter')
        self.midiout, self.portname_out = open_midioutput('Fighter')
        self.midiin.set_callback(self.event)
        self.midi_translation = class_midi_translation()
        self.state = UltraDict(name='state')
        self.fighter_mapping = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

    def event(self, event, data=None):
        message, deltatime = event
        print('\033[K', end='')  # Clear line
        print(f"\r{message[2]/127:.3f}", end='', flush=True)

        if message[1] in self.fighter_mapping:
            midi_index = self.fighter_mapping.index(message[1])
            self.midi_translation.update_context(midi_index, message[2])

    def update(self):
        values = self.midi_translation.get_context_midi_values()
        print(values)
        midi_values = [int(v * 127) for v in values]

        for i in range(16):
            # Set value and color based on whether encoder is active
            value = midi_values[i] if i < len(values) else 0
            color = 80 if i < len(values) else 30
            
            self.midiout.send_message([176, self.fighter_mapping[i], value])
            self.midiout.send_message([177, self.fighter_mapping[i], color])
