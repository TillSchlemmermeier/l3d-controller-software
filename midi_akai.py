import time as time
from rtmidi.midiutil import open_midiinput,open_midioutput, open_midiport

class class_akai:
    def __init__(self, array):
        # open midi input
        self.midiin, self.portname_in = open_midiinput(port = 'MIDI Mix')

        # set callback
        self.midiin.set_callback(self.event)
        self.global_parameter = array

    def event(self, event, data=None):
        """Call gets midi message and calls the mapping routine"""
        message, deltatime = event

        # print(message)
        # faders are 19, 23, 27, 31, 49, 53, 57, 61,62

        # global brightness
        if message[1] == 62:
            self.global_parameter[1] = message[2]/127.0
        # channel brightness
        elif message[1] == 49:
            self.global_parameter[41] = message[2]/127.0
        elif message[1] == 53:
            self.global_parameter[71] = message[2]/127.0
        elif message[1] == 57:
            self.global_parameter[101] = message[2]/127.0
        elif message[1] == 61:
            self.global_parameter[131] = message[2]/127.0
        # channel fade
        elif message[1] == 19:
            self.global_parameter[42] = message[2]/127.0
        elif message[1] == 23:
            self.global_parameter[72] = message[2]/127.0
        elif message[1] == 27:
            self.global_parameter[102] = message[2]/127.0
        elif message[1] == 31:
            self.global_parameter[132] = message[2]/127.0
        # channel strobo
        elif message[1] == 18:
            self.global_parameter[43] = message[2]/127.0
        elif message[1] == 22:
            self.global_parameter[73] = message[2]/127.0
        elif message[1] == 26:
            self.global_parameter[103] = message[2]/127.0
        elif message[1] == 30:
            self.global_parameter[133] = message[2]/127.0

        # s2l
        elif message[1] == 16:
            self.global_parameter[10] = message[2]/127.0
        elif message[1] == 20:
            self.global_parameter[11] = message[2]/127.0
        elif message[1] == 24:
            self.global_parameter[12] = message[2]/127.0
        elif message[1] == 28:
            self.global_parameter[13] = message[2]/127.0

        # s2l threshold
        elif message[1] == 17:
            self.global_parameter[14] = message[2]/127.0
        elif message[1] == 21:
            self.global_parameter[15] = message[2]/127.0
        elif message[1] == 25:
            self.global_parameter[16] = message[2]/127.0
        elif message[1] == 29:
            self.global_parameter[17] = message[2]/127.0

        # s2l normlizing trigger
        elif message[1] == 46:
            self.global_parameter[18] = message[2]/127.0

        # autopilot time
        elif message[1] == 58:
            self.global_parameter[6] = message[2]/127.0
