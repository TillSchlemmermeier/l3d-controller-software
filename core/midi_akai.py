import time as time
from rtmidi.midiutil import open_midiinput,open_midioutput, open_midiport

from midi_translation import class_midi_translation

class class_akai:
    def __init__(self, state):
        print('...starting AKAI MIDI controller')
        # open midi input
        self.midiin, self.portname_in = open_midiinput(port = 'MIDI Mix')

        # set callback
        self.midiin.set_callback(self.event)
        self.midi_translation = class_midi_translation(state)

    def event(self, event, data=None):
        """Call gets midi message and calls the mapping routine"""
        message, deltatime = event

        # cc messages
        if message[0] == 176:
            # global brightness
            if message[1] == 62:
                self.midi_translation.update_fixed(8, 'brightness', message[2])

            # channel brightness
            elif message[1] == 19:
                self.midi_translation.update_fixed(0, 'brightness', message[2])
            elif message[1] == 23:
                self.midi_translation.update_fixed(1, 'brightness', message[2])
            elif message[1] == 27:
                self.midi_translation.update_fixed(2, 'brightness', message[2])
            elif message[1] == 31:
                self.midi_translation.update_fixed(3, 'brightness', message[2])
            elif message[1] == 49:
                self.midi_translation.update_fixed(4, 'brightness', message[2])
            elif message[1] == 53:
                self.midi_translation.update_fixed(5, 'brightness', message[2])
            elif message[1] == 57:
                self.midi_translation.update_fixed(6, 'brightness', message[2])
            elif message[1] == 61:
                self.midi_translation.update_fixed(7, 'brightness', message[2])

            # channel fade
            elif message[1] == 18:
                self.midi_translation.update_fixed(0, 'fade', message[2])
            elif message[1] == 22 and message[0] == 176:
                self.midi_translation.update_fixed(1, 'fade', message[2])
            elif message[1] == 26:
                self.midi_translation.update_fixed(2, 'fade', message[2])
            elif message[1] == 30:
                self.midi_translation.update_fixed(3, 'fade', message[2])
            elif message[1] == 48:
                self.midi_translation.update_fixed(4, 'fade', message[2])
            elif message[1] == 52:
                self.midi_translation.update_fixed(5, 'fade', message[2])
            elif message[1] == 56:
                self.midi_translation.update_fixed(6, 'fade', message[2])
            elif message[1] == 60:
                self.midi_translation.update_fixed(7, 'fade', message[2])

            # parameters
            elif message[1] == 16:
                self.midi_translation.update_context(0, message[2])
            elif message[1] == 20:
                self.midi_translation.update_context(1, message[2])
            elif message[1] == 24:
                self.midi_translation.update_context(2, message[2])
            elif message[1] == 28:
                self.midi_translation.update_context(3, message[2])
            elif message[1] == 46:
                self.midi_translation.update_context(4, message[2])
            elif message[1] == 50:
                self.midi_translation.update_context(5, message[2])
            elif message[1] == 54:
                self.midi_translation.update_context(6, message[2])
            elif message[1] == 58:
                self.midi_translation.update_context(7, message[2])

            # channel IO
            if message[2] > 0:
                if message[1] == 3:
                    self.midi_translation.toggle_fixed(0, 'IO')
                elif message[1] == 6:
                    self.midi_translation.toggle_fixed(1, 'IO')
                elif message[1] == 9:
                    self.midi_translation.toggle_fixed(2, 'IO')
                elif message[1] == 12:
                    self.midi_translation.toggle_fixed(3, 'IO')
                elif message[1] == 15:
                    self.midi_translation.toggle_fixed(4, 'IO')
                elif message[1] == 18:
                    self.midi_translation.toggle_fixed(5, 'IO')
                elif message[1] == 21:
                    self.midi_translation.toggle_fixed(6, 'IO')
                elif message[1] == 24:
                    self.midi_translation.toggle_fixed(7, 'IO')

        # nt messages
        elif message[0] == 144:
            # oneshots
            if message[1] == 1:
                self.midi_translation.oneshot(1)
            elif message[1] == 4:
                self.midi_translation.oneshot(2)
            elif message[1] == 7:
                self.midi_translation.oneshot(3)
            elif message[1] == 10:
                self.midi_translation.oneshot(4)
            elif message[1] == 13:
                self.midi_translation.oneshot(5)
            elif message[1] == 16:
                self.midi_translation.oneshot(6)
            elif message[1] == 19:
                self.midi_translation.oneshot(7)
            elif message[1] == 22:
                self.midi_translation.oneshot(8)

