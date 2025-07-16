import time as time
from rtmidi.midiutil import open_midiinput,open_midioutput, open_midiport
from midi_translation import class_midi_translation
from UltraDict import UltraDict

class class_launchcontrol:
    def __init__(self):
        """initializes the MIDI fighter"""

        self.midiin, self.portname_in = open_midiinput('LCXL3 1 MIDI In')
        self.midiout, self.portname_out = open_midioutput(1)
        self.midiin.set_callback(self.event)
        self.midi_translation = class_midi_translation()
        # self.list_available_devices()

    def list_available_devices(self):
        import rtmidi
    
        # List MIDI Input devices
        midiin = rtmidi.MidiIn()
        print("Available MIDI Input devices:")
        for i, port_name in enumerate(midiin.get_ports()):
            print(f"  {i}: {port_name}")
        
        # List MIDI Output devices
        midiout = rtmidi.MidiOut()
        print("\nAvailable MIDI Output devices:")
        for i, port_name in enumerate(midiout.get_ports()):
            print(f"  {i}: {port_name}")


    def event(self, event, data=None):
        message, deltatime = event
        print("Received MIDI message:", message)

        # cc messages
        if message[0] == 176:
            # global brightness
            if message[1] == 62:
                self.midi_translation.update_fixed(8, 'brightness', message[2])

            # channel brightness
            elif message[1] == 5:
                self.midi_translation.update_fixed(0, 'brightness', message[2])
            elif message[1] == 6:
                self.midi_translation.update_fixed(1, 'brightness', message[2])
            elif message[1] == 7:
                self.midi_translation.update_fixed(2, 'brightness', message[2])
            elif message[1] == 8:
                self.midi_translation.update_fixed(3, 'brightness', message[2])
            elif message[1] == 9:
                self.midi_translation.update_fixed(4, 'brightness', message[2])
            elif message[1] == 10:
                self.midi_translation.update_fixed(5, 'brightness', message[2])
            elif message[1] == 11:
                self.midi_translation.update_fixed(6, 'brightness', message[2])
            elif message[1] == 12:
                self.midi_translation.update_fixed(7, 'brightness', message[2])

            # channel fade
            elif message[1] == 29:
                self.midi_translation.update_fixed(0, 'fade', message[2])
            elif message[1] == 30:
                self.midi_translation.update_fixed(1, 'fade', message[2])
            elif message[1] == 31:
                self.midi_translation.update_fixed(2, 'fade', message[2])
            elif message[1] == 32:
                self.midi_translation.update_fixed(3, 'fade', message[2])
            elif message[1] == 33:
                self.midi_translation.update_fixed(4, 'fade', message[2])
            elif message[1] == 34:
                self.midi_translation.update_fixed(5, 'fade', message[2])
            elif message[1] == 35:
                self.midi_translation.update_fixed(6, 'fade', message[2])
            elif message[1] == 36:
                self.midi_translation.update_fixed(7, 'fade', message[2])

            # parameters
            elif message[1] == 13:
                self.midi_translation.update_context(0, message[2])
            elif message[1] == 14:
                self.midi_translation.update_context(1, message[2])
            elif message[1] == 15:
                self.midi_translation.update_context(2, message[2])
            elif message[1] == 16:
                self.midi_translation.update_context(3, message[2])
            elif message[1] == 17:
                self.midi_translation.update_context(4, message[2])
            elif message[1] == 18:
                self.midi_translation.update_context(5, message[2])
            elif message[1] == 19:
                self.midi_translation.update_context(6, message[2])
            elif message[1] == 20:
                self.midi_translation.update_context(7, message[2])

            # channel IO
            elif message[1] == 37:
                self.midi_translation.toggle_fixed(0, 'IO')
            elif message[1] == 38:
                self.midi_translation.toggle_fixed(1, 'IO')
            elif message[1] == 39:
                self.midi_translation.toggle_fixed(2, 'IO')
            elif message[1] == 40:
                self.midi_translation.toggle_fixed(3, 'IO')
            elif message[1] == 41:
                self.midi_translation.toggle_fixed(4, 'IO')
            elif message[1] == 42:
                self.midi_translation.toggle_fixed(5, 'IO')
            elif message[1] == 43:
                self.midi_translation.toggle_fixed(6, 'IO')
            elif message[1] == 44:
                self.midi_translation.toggle_fixed(7, 'IO')

        # nt messages
        # elif message[0] == 144:
        #     # oneshots
        #     if message[1] == 1:
        #         self.midi_translation.oneshot(1)
        #     elif message[1] == 4:
        #         self.midi_translation.oneshot(2)
        #     elif message[1] == 7:
        #         self.midi_translation.oneshot(3)
        #     elif message[1] == 10:
        #         self.midi_translation.oneshot(4)
        #     elif message[1] == 13:
        #         self.midi_translation.oneshot(5)
        #     elif message[1] == 16:
        #         self.midi_translation.oneshot(6)
        #     elif message[1] == 19:
        #         self.midi_translation.oneshot(7)
        #     elif message[1] == 22:
        #         self.midi_translation.oneshot(8)

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
        # values = self.midi_translation.get_context_midi_values()
        # print(values)
        # midi_values = [int(v * 127) for v in values]

        # for i in range(16):
        #     # Set value and color based on whether encoder is active
        #     value = midi_values[i] if i < len(values) else 0
        #     color = 80 if i < len(values) else 30
            
        #     self.midiout.send_message([176, self.fighter_mapping[i], value])
        #     self.midiout.send_message([177, self.fighter_mapping[i], color])
