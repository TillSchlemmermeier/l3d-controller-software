import time as time
from rtmidi.midiutil import open_midiinput,open_midioutput, open_midiport

class class_fighter:
    def __init__(self, array):
        """initializes the MIDI fighter"""

        self.global_parameter = array

        # initialize variables
        # self.current_state contains the state information as a vector with
        # the length of the number of channels
        # 0 - generator state
        # 1 - effect 1 state
        # 2 - effect 2 state
        # 3 - effect 3 state
        # 4 - modifiyng global effect
        self.current_state = [0, 0, 0, 0]

        # initialize midi input
        # self.input_port = in_port
        self.midiin, self.portname_in = open_midiinput('Fighter')

        # initialize midi output
        # self.output_port = out_port
        self.midiout, self.portname_out = open_midioutput('Fighter')

        # initializes the callback
        self.midiin.set_callback(self.event)
        self.sendstate()

        print('figher init ist durch!')

    def event(self, event, data=None):
        """Call gets midi message and calls the mapping routine"""

        if event[0] == 'T':
            self.current_state[event[1]] = event[2]
            self.sendstate()
        else:
            # gets message
            message, deltatime = event

            # figure out the mapping
            key = self.setParameters(message[0], message[1], message[2])

            # if there is no state-switch, write the value into
            # the global variable - all values go from 0 - 1
            if key != []:
                self.global_parameter[key[0]] = key[1]/127.0
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
        # 0 - 3: channel specific colors
        # 4 - 6: colors for global effects
        # 7    : off
        color_dict = {0:70, 1:61, 2:50, 3:20, 4: 61, 5: 50, 6: 20, 7: 0}
        # print('state of fighter:', self.current_state)

        # now we want to send the current values back!
        # colors as well as current values!

        # loop through first column
        for i in [0, 4, 8, 12]:
            self.midiout.send_message([177, i, color_dict[self.current_state[0]]])
            # calculate the position of the corresponding entry in the global variable
            index = int(45+self.current_state[0]*5+i/4)
            value = int(self.global_parameter[index]*127)
            self.midiout.send_message([176, i, value])
        # second column
        for i in [1, 5, 9, 13]:
            self.midiout.send_message([177, i, color_dict[self.current_state[1]]])
            index = int(75+self.current_state[1]*5+i/4)
            value = int(self.global_parameter[index]*127)
            self.midiout.send_message([176, i, value])

        for i in [2, 6, 10, 14]:
            self.midiout.send_message([177, i, color_dict[self.current_state[2]]])
            index = int(105+self.current_state[2]*5+i/4)
            value = int(self.global_parameter[index]*127)
            self.midiout.send_message([176, i, value])

        for i in [3, 7, 11, 15]:
            self.midiout.send_message([177, i, color_dict[self.current_state[3]]])
            index = int(135+self.current_state[3]*5+i/4)
            value = int(self.global_parameter[index]*127)
            # print(i, value, self.current_state[3])
            self.midiout.send_message([176, i, value])


    def setParameters(self, channel, key, value):
        """Routine to map the incomming midi values to the
        correct position in the global variable

        return empty list when state is switched, otherwise
        [position, value]
        """

        '''
        Master Controls
        16-17-18-19
        20-21-22-23
        24-25-26-27
        28-29-30-31
        '''
        # check for state switches
        if channel == 177:
            self.setstate(key, value)
#            print(self.global_parameter[200:205])
            return []
        else:
            # write master commands for each channel
            if key in [16,20,24,28]:     # channel 1
                basic_index = 40
                state = 0
            elif key in [17,21,25,29]:   # channel 2
                basic_index = 70
                state = 0
            elif key in [18,22,26,30]:  # channel 3
                basic_index = 100
                state = 0
            elif key in [19,23,27,31]:  # channel 4
                basic_index = 130
                state = 0

            # get position to write for each channel
            if key in [0, 4, 8, 12]:     # channel 1
                if self.current_state[0] < 4:
                    state = self.current_state[0]
                    basic_index = 45
                else:
                    state = 0 # self.current_state[0]
                    basic_index = 234

            elif key in [1, 5, 9, 13]:   # channel 2
                if self.current_state[1] < 4:
                    basic_index = 75
                    state = self.current_state[1]
                else:
                    state = 0 # self.current_state[0]
                    basic_index = 238

            elif key in [2, 6, 10, 14]:  # channel 3
                if self.current_state[1] < 4:
                    basic_index = 105
                    state = self.current_state[2]
                else:
                    state = 0 # self.current_state[0]
                    basic_index = 242

            elif key in [3, 7, 11, 15]:  # channel 4
                basic_index = 135
                state = self.current_state[3]

            if key in [0, 1, 2, 3]:         # generators
                key = 0
            elif key in [4, 5, 6, 7]:       # effect 1
                key = 1
            elif key in [8, 9, 10, 11]:     # effect 2
                key = 2
            elif key in [12, 13, 14, 15]:   # effect 3
                key = 3
            elif key in [16, 17,18, 19]:    # Master C 1
                key = 0
            elif key in [20, 21, 22, 23]:   #;Master C 2
                key = 1
            elif key in [24, 25, 26, 27]:   # Master C 3
                key = 2
            elif key in [28, 29, 30, 31]:   # Master C 4
                key = 3

            # return [position in global variable, key]
            # print('index: '+str(basic_index + state*5 + key)+'value: '+str(value))
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

        for i in range(4):
            self.global_parameter[201+i] = self.current_state[i]
