from rtmidi.midiutil import open_midiinput,open_midioutput
from midi.translation import MidiTranslation


class LaunchControl:
    def __init__(self, state):
        """initializes the Launch Control"""

        self.midiin, self.portname_in = open_midiinput('LCXL3 1 MIDI In')
        self.midiout, self.portname_out = open_midioutput(1)
        self.midiin.set_callback(self.event)
        self.midi_translation = MidiTranslation(state)

    def event(self, event, data=None):
        message, deltatime = event

        # cc messages
        if message[0] == 176:
            cc, value = message[1], message[2]

            # global brightness
            if cc == 36:
                self.midi_translation.update_fixed(8, 'brightness', value)

            # channel brightness on CC 5-12, channel fade on CC 29-35
            if 5 <= cc <= 12:
                self.midi_translation.update_fixed(cc - 5, 'brightness', value)
            elif 29 <= cc <= 35:
                self.midi_translation.update_fixed(cc - 29, 'fade', value)

            # oneshots 1-8 on CC 45-52
            if 45 <= cc <= 52:
                self.midi_translation.oneshot(cc - 44)

            # parameters: four knobs per context, CC 13-28
            elif 13 <= cc <= 28:
                self.midi_translation.update_context((cc - 13) // 4, (cc - 13) % 4, value)

            # channel IO on CC 37-44
            elif 37 <= cc <= 44: # and value > 0:
                self.midi_translation.toggle_fixed(cc - 37, 'IO')

    def update(self):
        print("Updating Launch Control")
        for i in range(8):
            cc_number = 13 + i
            # Send color value (0-127, different values = different colors)
            # Red = 5, Green = 17, Blue = 41, Yellow = 13, etc.
            color_value = 17  # Green
            self.midiout.send_message([176, cc_number, color_value])
        
        # Bottom row knobs (CC 29-36) - LED ring colors  
        for i in range(8):
            cc_number = 29 + i
            color_value = 5  # Red
            self.midiout.send_message([176, cc_number, color_value])
        
        # Send LED colors for buttons (Focus buttons CC 37-44)
        for i in range(8):
            cc_number = 37 + i
            # Button LED colors: 0=off, 1-3=red shades, 17-19=green shades, etc.
            button_color = 17  # Green
            self.midiout.send_message([176, cc_number, button_color])
