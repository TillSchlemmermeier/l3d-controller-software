
import time as time
from rtmidi.midiutil import open_midiinput,open_midioutput, open_midiport
#from rtmidi.midiconstants import NOTE_ON, NOTE_OFF,CONTROL_CHANGE
#from global_parameter_module import global_parameter
import numpy as np

class class_launchpad_mk3:
    def __init__(self, array):
        # open midi input
        self.midiin, self.portname_in = open_midiinput(port= '28:1')
        self.midiout, self.portname_out = open_midioutput(port = '28:1')
        self.global_parameter = array
        # turn leds off
        for i, c in zip(range(11,88), range(0,88-11)):
            self.midiout.send_message([144, i, c/1])

        # set callback
        self.midiin.set_callback(self.event)
        # array for state switching
        # states are preset, generator, effect1, effect2, effect3 for
        # each channel, which makes 20 states + idle state
        self.state = 0	 # this is the idle state
        self.sendstate() # send the current state to launchpad

    def event(self, event, data=None):
        """Call gets midi message and calls the mapping routine"""
        # gets message from midi input
        message, deltatime = event
        print(message)

        # switch channels on
        # this are the round buttons at the top
        if message[0] == 176:
            if message[1]   == 91 and message[2] == 127:
                self.global_parameter[40] = int(not self.global_parameter[40])
            elif message[1] == 92 and message[2] == 127:
                self.global_parameter[70] = int(not self.global_parameter[70])
            elif message[1] == 93 and message[2] == 127:
                self.global_parameter[100] = int(not self.global_parameter[100])
            elif message[1] == 94 and message[2] == 127:
                self.global_parameter[130] = int(not self.global_parameter[130])

        # parse message
        elif message[0] == 144 and message[2] == 0:
            print('')
            print('message', message)
            print('state before', self.state)
            if self.state == 0:
                # if in idle state, state can be switched
                key = [9-int(message[1]*0.1), message[1]%10]

                # check whether button is in range
                if key[0] <= 5 and key[1] <= 4:
                    self.state = key
            #        print(self.state)
            else:
                # if not idle, we can go back to idle
                # this is to close the selection matrix
                # self.state[0] ist reihe
                # self.state[1] ist spalte
                if message[1] == 81:
                    print('close menu')
                    self.state = 0
                else:
                    # check for presets
                    if self.state[0] == 1:
                        print('no stored presets...')
                    else:
                        index = 18 + (self.state[1]-1)*5 + self.state[0]

                        # addition
                        add = -82 + (8-int(message[1]*0.1))*18

                        self.global_parameter[index] = message[1]+add
                        print('launchpad sets: ', index, self.global_parameter[index])

        # send colors and state at the end
        self.sendstate()
        print('state after', self.state)

    def convert(self, number):
        """
        converts numbers to correct range
        this is not used at the moment...
        """
        correction = int(number/8)*8 / 2.0
        return number - correction


    def sendstate(self):
        """send states and colors to midi device"""
        # send the state to a global parameter entry
        # state 0 is closed
        # get starting number of channel
        if self.state == 0:
            self.global_parameter[4] = 0
        else:
            channel_number = self.state[0]*4
            self.global_parameter[4] = channel_number*self.state[1]
            # print('launchpad state:', self.state)

        # first, turn all leds off
        for i in range(11,89):
            self.midiout.send_message([144, i, 0])

        print(self.global_parameter[ 40])
        # send the state of the channel switches (on/off)
        self.midiout.send_message([176, 91, self.global_parameter[ 40]*127])
        self.midiout.send_message([176, 92, self.global_parameter[ 70]*127])
        self.midiout.send_message([176, 93, self.global_parameter[100]*127])
        self.midiout.send_message([176, 94, self.global_parameter[130]*127])


        # if idle state, we can open the selection menu
        if self.state == 0:
            for i in range(4):
                self.midiout.send_message([144, 81+i, 10])
                self.midiout.send_message([144, 71+i, 20])
                self.midiout.send_message([144, 61+i, 30])
                self.midiout.send_message([144, 51+i, 40])
                self.midiout.send_message([144, 41+i, 50])

        else:
            # select color
            if self.state[0] == 1:
                color = 10
            elif self.state[0] == 2:
                color = 20
            elif self.state[0] == 3:
                color = 30
            elif self.state[0] == 4:
                color = 40
            elif self.state[0] == 5:
                color = 50
            else:
                color = 0

            # send color
            for i in range(11,89):
                self.midiout.send_message([144, i, color])

            self.midiout.send_message([144, 81, 1])


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

class class_launchpad:
    def __init__(self,array):
        # open midi input
        self.midiin, self.portname_in = open_midiinput(port = 'Launchpad')
        self.midiout, self.portname_out = open_midioutput(port = 'Launchpad')
        self.global_parameter = array
        # turn leds off
        for i in range(130):
            self.midiout.send_message([144, i, 0])

        # set callback
        self.midiin.set_callback(self.event)
        # array for state switching
        # states are preset, generator, effect1, effect2, effect3 for
        # each channel, which makes 20 states + idle state
        self.state = 0	 # this is the idle state
        self.sendstate() # send the current state to launchpad

    def event(self, event, data=None):
        """Call gets midi message and calls the mapping routine"""
        # gets message from midi input
        message, deltatime = event

        # switch channels on
        # this are the round buttons at the top
        if message[0] == 176:
            if message[1]   == 104 and message[2] == 127:
                self.global_parameter[40] = int(not self.global_parameter[40])
            elif message[1] == 105 and message[2] == 127:
                self.global_parameter[70] = int(not self.global_parameter[70])
            elif message[1] == 106 and message[2] == 127:
                self.global_parameter[100] = int(not self.global_parameter[100])
            elif message[1] == 107 and message[2] == 127:
                self.global_parameter[130] = int(not self.global_parameter[130])

        # parse message
        elif message[0] == 144 and message[2] == 0:
            if self.state == 0:
                # if in idle state, state can be switched
                key = [int(message[1]/16), message[1]-16*int(message[1]/16)]
                # check whether button is in range
                if key[0] < 5 and key[1] < 4:
                    self.state = key
            else:
                # if not idle, we can go back to idle
                # this is to close the selection matrix
                if message[1] == 0:
                    self.state = 0
                else:
                    # check for presets
                    if self.state[0] == 0:
                        print('no stored presets...')
                    else:
                        index = 19 + self.state[0] + 5* self.state[1]
                        self.global_parameter[index] = int(self.convert(message[1])-1)
                        print('launchpad sets: ', index, self.global_parameter[index])

        # send colors and state at the end
        self.sendstate()

    def sendstate(self):
        """send states and colors to midi device"""
        # send the state to a global parameter entry
        # state 0 is closed
        # get starting number of channel
        if self.state == 0:
            self.global_parameter[4] = 0
        else:
            channel_number = self.state[0]*4
            self.global_parameter[4] = channel_number*self.state[1]
            print('launchpad state:', self.state)

        # first, turn all leds off
        for i in range(130):
            self.midiout.send_message([144, i, 0])

        # send the state of the channel switches (on/off)
        self.midiout.send_message([176, 104, self.global_parameter[ 40]*127])
        self.midiout.send_message([176, 105, self.global_parameter[ 70]*127])
        self.midiout.send_message([176, 106, self.global_parameter[100]*127])
        self.midiout.send_message([176, 107, self.global_parameter[130]*127])

        # if idle state, we can open the selection menu
        if self.state == 0:
            for i in range(4):
                self.midiout.send_message([144, i, 3])
                self.midiout.send_message([144, i+16, 51])
                self.midiout.send_message([144, i+32, 48])
                self.midiout.send_message([144, i+48, 3])
                self.midiout.send_message([144, i+64, 51])
        else:
            # select color
            if self.state[0] == 0:
                color = 3
            elif self.state[0] == 1:
                color = 51
            elif self.state[0] == 2:
                color = 48
            elif self.state[0] == 3:
                color = 3
            elif self.state[0] == 4:
                color =  51
            else:
                color = 0

            # send color
            for i in range(130):
                self.midiout.send_message([144, i, color])

            self.midiout.send_message([144, 0, 1])

    def convert(self, number):
        """
        converts numbers to correct range
        this is not used at the moment...
        """
        correction = int(number/8)*8 / 2.0
        return number - correction


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
            # pass

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

        # loop through first column
        for i in [0, 4, 8, 12]:
            self.midiout.send_message([177, i, color_dict[self.current_state[0]]])
            # calculate the position of the corresponding entry in the global variable
            index = int(45+self.current_state[0]*5+i/4)
            value = int(self.global_parameter[index]*127)
            self.midiout.send_message([176, i, value])
        for i in [1, 5, 9, 13]:
            self.midiout.send_message([177, i, color_dict[self.current_state[1]]])
            index = int(75+self.current_state[1]*5+i/4)
            value = int(self.global_parameter[index]*127)
            self.midiout.send_message([176, i, value])
        for i in [2, 6,10, 14]:
            self.midiout.send_message([177, i, color_dict[self.current_state[2]]])
            index = int(105+self.current_state[2]*5+i/4)
            value = int(self.global_parameter[index]*127)
            self.midiout.send_message([176, i, value])
        for i in [3, 7,11, 15]:
            self.midiout.send_message([177, i, color_dict[self.current_state[3]]])
            index = int(135+self.current_state[3]*5+i/4)
            value = int(self.global_parameter[index]*127)
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
                basic_index = 45
                state = self.current_state[0]
            elif key in [1, 5, 9, 13]:   # channel 2
                basic_index = 75
                state = self.current_state[1]
            elif key in [2, 6, 10, 14]:  # channel 3
                basic_index = 105
                state = self.current_state[2]
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
            #print('index: '+str(basic_index + state*5 + key)+'value: '+str(value))
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
