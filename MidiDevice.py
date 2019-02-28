
import time as time
from rtmidi.midiutil import open_midiinput,open_midioutput
#from rtmidi.midiconstants import NOTE_ON, NOTE_OFF,CONTROL_CHANGE
from global_parameter_module import global_parameter


class class_fighter:
    def __init__(self, in_port, out_port):
        """initializes the MIDI fighter"""

        # initialize variables
        # self.current_state contains the state information as a vector with
        # the length of the number of channels
        # 0 - generator state
        # 1 - effect 1 state
        # 2 - effect 2 state
        # 3 - effect 3 state
        self.current_state = [0, 0, 0, 0]

        # initialize midi input
        self.input_port = in_port
        self.midiin, self.portname_in = open_midiinput(self.input_port)

        # initialize midi output
        self.output_port = out_port
        self.midiout, self.portname_out = open_midioutput(self.output_port)

        # initializes the callback
        self.midiin.set_callback(self.event)
        self.sendstate()

    def event(self, event, data=None):
        """Call gets midi message and calls the mapping routine"""
        # gets message
        message, deltatime = event

        # figure out the mapping
        key = self.setParameters(message[0], message[1], message[2])

        # if there is no state-switch, write the value into
        # the global variable - all values go from 0 - 1
        if key != []:
            global_parameter[key[0]] = key[1]/127.0
        else:
            # when a stateswitch is detected, send all values
            # and colors back to midifighter
            self.sendstate()

    def sendstate(self):
        """Sends colors and values to MidiFighter"""
        # this contains the colors for the three different states
        # generator : color 0
        # effect 1  : color 40
        # effect 2  : color 80
        # effect 3  : color 120
        color_dict = {0:10, 1:50, 2:70, 3:100}

        # now we want to send the current values back!
        # colors as well as current values!
        for i in [0, 4, 8, 12]:
            self.midiout.send_message([177, i, color_dict[self.current_state[0]]])
            # calculate the position of the corresponding entry in the global variable
            index = int(50+self.current_state[0]*5+i/4)
            value = int(global_parameter[index]*127)
            self.midiout.send_message([176, i, value])
        for i in [1, 5, 9, 13]:
            self.midiout.send_message([177, i, color_dict[self.current_state[1]]])
            index = int(70+self.current_state[1]*5+i/4)
            value = int(global_parameter[index]*127)
            self.midiout.send_message([176, i, value])
        for i in [2, 6,10, 14]:
            self.midiout.send_message([177, i, color_dict[self.current_state[2]]])
            index = int(100+self.current_state[2]*5+i/4)
            value = int(global_parameter[index]*127)
            self.midiout.send_message([176, i, value])
        for i in [3, 7,11, 15]:
            self.midiout.send_message([177, i, color_dict[self.current_state[3]]])
            index = int(130+self.current_state[3]*5+i/4)
            value = int(global_parameter[index]*127)
            self.midiout.send_message([176, i, value])


    def setParameters(self, channel, key, value):
        """Routine to map the incomming midi values to the
        correct position in the global variable

        return empty list when state is switched, otherwise
        [position, value]
        """

        # check for state switches
        if channel == 177:
            self.setstate(key, value)
            return []
        else:
            # get position to write for each channel
            if key in [0, 4, 8, 12]:     # channel 1
                basic_index = 45
                state = self.current_state[0]
            elif key in [1, 5, 9, 13]:   # channel 2
                basic_index = 70
                state = self.current_state[1]
            elif key in [2, 6, 10, 14]:  # channel 3
                basic_index = 100
                state = self.current_state[2]
            elif key in [3, 7, 11, 15]:  # channel 4
                basic_index = 130
                state = self.current_state[3]

            if key in [0, 1, 2, 3]:         # generators
                key = 0
            elif key in [4, 5, 6, 7]:       # effect 1
                key = 1
            elif key in [8, 9, 10, 11]:     # effect 2
                key = 2
            elif key in [12, 13, 14, 15]:   # effect 3
                key = 3

            # return [position in global variable, key]
            return [basic_index + state*5 + key, value]

    def setstate(self, key, value):
        """check for state switches"""
        if key in [0, 4, 8, 12]:     # channel 1
            if key == 0 and value == 0:
                self.current_state[0] = 0
            elif key == 4 and value == 0:
                self.current_state[0] = 1
            elif key == 8 and value == 0:
                self.current_state[0] = 2
            elif key == 12 and value == 0:
                self.current_state[0] = 3

        elif key in [1, 5, 9, 13]:   # channel 2
            if key == 1 and value == 0:
                self.current_state[1] = 0
            elif key == 5 and value == 0:
                self.current_state[1] = 1
            elif key == 9 and value == 0:
                self.current_state[1] = 2
            elif key == 13 and value == 0:
                self.current_state[1] = 3

        elif key in [2, 6, 10, 14]:  # channel 3
            if key == 2 and value == 0:
                self.current_state[2] = 0
            elif key == 6 and value == 0:
                self.current_state[2] = 1
            elif key == 10 and value == 0:
                self.current_state[2] = 2
            elif key == 14 and value == 0:
                self.current_state[2] = 3

        elif key in [3, 7, 11, 15]:  # channel 4
            if key == 3 and value == 0:
                self.current_state[3] = 0
            elif key == 7 and value == 0:
                self.current_state[3] = 1
            elif key == 11 and value == 0:
                self.current_state[3] = 2
            elif key == 15 and value == 0:
                self.current_state[3] = 3



'''
class MidiInputHandler: #(object):
    def __init__(self, port):
        """Initializes the input handler,
        which gets the midi input via callback and
        passes it to the global variable
        """
        self.port = port                # what is this for?
        self._wallclock = time.time()   # we also don't need this
        self.mapping = GlobalParameterHandler()

    def __call__(self, event, data=None):
        """Call gets midi message and calls the mapping routine"""
        message, deltatime = event
        self._wallclock += deltatime

        # figure out the mapping
        key = self.mapping.setParameters(message[0], message[1], message[2])
        # if there is no state-switch, write the value into
        # the global variable - all values go from 0 - 1
        if key != []:
            global_parameter[key[0]] = key[1]/127.0




class MidiDevice:
    """Initializes the MIDI input and enables communication with the
    MIDI Device
    """
    def __init__(self, in_port, out_port):
        print("Initialize MIDI CONTROL")
#        global input_dict
        self.input_port = in_port
        self.midiin, self.portname_in = open_midiinput(self.input_port)
        self.Handler = MidiInputHandler(self.portname_in)
        self.midiin.set_callback(self.Handler)

        self.output_port = out_port
        self.midiout, self.portname_out = open_midioutput(self.output_port)

        self.color = 0x01

        self.cc0 = CONTROL_CHANGE | 0x00
        self.cc1 = CONTROL_CHANGE | 0x01
        self.cc2 = CONTROL_CHANGE | 0x02
        self.cc3 = CONTROL_CHANGE | 0x03
        self.cc4 = CONTROL_CHANGE | 0x04
        self.cc5 = CONTROL_CHANGE | 0x05
        self.cc6 = CONTROL_CHANGE | 0x06
        self.cc8 = CONTROL_CHANGE | 0x08
        self.makeRingBlink(0x00)
        self.makeRingBlink(0x04)
        self.makeRingBlink(0x08)
        self.makeRingBlink(0x0B)
        self.makeRainbow(0x01)
        self.makeLedBlink(0x05)
        self.stopBlink(0x0B)
        #time.sleep(1)
        #self.midiout.send_message([0xB2,0x00,0x3C])
        #time.sleep(1)
        #self.midiout.send_message([0xB3,0x00,0x04])


    def logMidi(self):
        print("Midi Channel :"+str(MidiChannelIn)+" | Midi Key :"+str(MidiKeyIn)+" | Midi Value : "+str(MidiValueIn))
        self.setRGB(0x03,self.color)
        self.color+=0x01
        root.after(500, test.logMidi)

#    def read(self):
#        return input_dict

    def send(self,Key,Value):
        self.midiout.send_message([self.cc0,Key,Value])

    def makeRingBlink(self,Key):
        self.midiout.send_message([0xB2,Key,0x3C])
        self.midiout.send_message([0xB3,Key,0x04])
    def makeRainbow(self,Key):
        self.midiout.send_message([0xB2,Key,0x7F])
    def makeLedBlink(self,Key):
        self.midiout.send_message([0xB2,Key,0x0C])
    def stopBlink(self,Key):
        self.midiout.send_message([0xB2,Key,0x00])
    def setRGB(self,Key,Color):
        self.midiout.send_message([0xB1,Key,Color])


'''
