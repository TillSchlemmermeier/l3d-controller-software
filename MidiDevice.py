
import time as time
from rtmidi.midiutil import open_midiinput,open_midioutput, open_midiport
#from rtmidi.midiconstants import NOTE_ON, NOTE_OFF,CONTROL_CHANGE
#from global_parameter_module import global_parameter
import numpy as np

class class_launchpad_mk3:
    def __init__(self, array):
        # open midi input
        self.midiin, self.portname_in = open_midiinput(port= ':1')
        self.midiout, self.portname_out = open_midioutput(port = ':1')
        self.global_parameter = array
        #activate programming mode
        self.midiout.send_message([240,0,32,41,2,13,14,1,247])
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

        # assemble list of parameters for presets, so that each channel
        # knows what belongs to him:
        # generator, effect1, effect2, effect3, effect, *parameters
        self.indices = []
        self.indices.append([20, 21, 22, 23] + [x for x in range( 40, 70)])
        self.indices.append([25, 26, 27, 28] + [x for x in range( 70,100)])
        self.indices.append([30, 31, 32, 33] + [x for x in range(100,130)])
        self.indices.append([35, 36, 37, 38] + [x for x in range(130,160)])


    def event(self, event, data=None):
        """Call gets midi message and calls the mapping routine"""
        # gets message from midi input
        message, deltatime = event
        #print(message)

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

        # check whether button was pressed
        elif message[0] == 144 and message[2] == 0:
            # parse message of launchpad
            # state == 0 : menu is closed
            # state == <int> : menu is open

            if self.state == 0:
                # if in idle state, state can be switched
                # and menu is openend
                key = [9-int(message[1]*0.1), message[1]%10]
                # key[1] defines the channel, starting at 1

                print(message)

                # start/stop cube
                if message[1] == 88:
                    if self.global_parameter[0] == 1:
                        self.global_parameter[0] = 0
                    else:
                        self.global_parameter[0] = 1
                        self.global_parameter[1] = 1
                        self.global_parameter[2] = 0.0
                        self.global_parameter[3] = 1.0
                        self.global_parameter[20] = 1
                        # activate channel 1
                        self.global_parameter[40] = 1
                        self.global_parameter[41] = 1
                        # activate channel 2
                        self.global_parameter[70] = 1


                    print(self.global_parameter[0])

                # check whether button is in range for menus
                if key[0] <= 5 and key[1] <= 4:
                    self.state = key

                    # now we have to send the current state to
                    # global variable
                    # send to global parameter array which menu is open
                    # we can hardcode this for testing

                    # check for channel
                    if key[1]-1 == 0:
                        self.global_parameter[200] = key[0]
                    elif key[1]-1 == 1:
                        self.global_parameter[200] = key[0]+5
                    elif key[1]-1 == 2:
                        self.global_parameter[200] = key[0]+10
                    elif key[1]-1 == 3:
                        self.global_parameter[200] = key[0]+15

                elif key[0] == 8:
                    print('saving preset for channel', key[1])
                    try:
                        self.save_preset(key[1])
                    except:
                        print('error saving preset!')

                elif key[0] == 7:
                    print('saving temporary preset for channel', key[1])
                    try:
                        self.save_preset(key[1], filename = 'temporary_preset.dat')
                    except:
                        print('error saving preset!')

                elif key[0] == 6:
                    print('loading temporary preset for channel', key[1])
                    try:
                        self.load_preset(-1, key[1], 'temporary_preset.dat')
                    except:
                        print('error loading temporary preset!')

            else:
                # if not idle, we can go back to idle
                # this is to close the selection matrix
                # self.state[0] ist reihe
                # self.state[1] ist spalte
                # why is this mixed with key?!
                if message[1] == 81:
                    # print('close menu')
                    self.state = 0
                    self.global_parameter[200] = 0

                else:
                    # check for presets
                    if self.state[0] == 1:
                        print('trying to load preset')
                        # figure out the state
                        index = 18 + (self.state[1]-1)*5 + self.state[0]

                        # addition
                        add = -82 + (8-int(message[1]*0.1))*18

                        try:
                            self.load_preset(preset_id = message[1]+add, channel = self.state[1])
                        except:
                            print('error loading preset')
#                        self.global_parameter[index] = message[1]+add

                    else:
                        # figure out the state
                        index = 18 + (self.state[1]-1)*5 + self.state[0]

                        # addition
                        add = -82 + (8-int(message[1]*0.1))*18

                        self.global_parameter[index] = message[1]+add
                        #print('launchpad sets: ', index, self.global_parameter[index])

        # send colors and state at the end
        self.sendstate()
        #print('state after', self.state)


    def save_preset(self, channel, filename = 'presets.dat'):
        '''appends the current values of a channel to a file
        channel goes from 1 to 4
        '''

        # assemble list of parameters
        list = []
        list.append('name')

        for i in self.indices[channel-1]:
            list.append(str(round(self.global_parameter[i], 2)))

        # save preset
        with open(filename, 'a+') as file:
            file.write(' '.join(list)+'\n')


    def load_preset(self, preset_id, channel, filename = 'presets.dat'):
        '''loads preset from file and writes to global array'''

        print(' preset id : ', preset_id)
        print(' channel   : ', channel)
        print(' file name : ', filename)

        with open(filename, 'r') as file:
            presets = file.readlines()

        try:
            preset = presets[preset_id].strip('\n').split()
            print('loading preset', preset[0])

            # write values into global parameter array
            # hopefully on the right place
            for i, value in zip(self.indices[channel-1], preset[1:]):
                # dont set channel on/off
                if i not in [40, 70, 100, 130]:
                    self.global_parameter[i] = float(value)

        except:
            print('preset not available')



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

        # print(self.global_parameter[ 40])
        # send the state of the channel switches (on/off)
        self.midiout.send_message([176, 91, self.global_parameter[ 40]*127])
        self.midiout.send_message([176, 92, self.global_parameter[ 70]*127])
        self.midiout.send_message([176, 93, self.global_parameter[100]*127])
        self.midiout.send_message([176, 94, self.global_parameter[130]*127])

        # if idle state, we can open the selection menu
        if self.state == 0:
            for i in range(4):
                self.midiout.send_message([144, 81+i,  5])
                self.midiout.send_message([144, 71+i, 61])
                self.midiout.send_message([144, 61+i, 13])
                self.midiout.send_message([144, 51+i, 21])
                self.midiout.send_message([144, 41+i, 37])

                # "copy" buttons
                self.midiout.send_message([144, 31+i, 45])
                self.midiout.send_message([144, 21+i, 54])

                # "save preset" button
                self.midiout.send_message([144, 11+i, 2])

                # on/off button
                self.midiout.send_message([144, 88, 2])
        else:
            # select color
            if self.state[0] == 1:
                color = 5
            elif self.state[0] == 2:
                color = 9
            elif self.state[0] == 3:
                color = 13
            elif self.state[0] == 4:
                color = 21
            elif self.state[0] == 5:
                color = 37
            else:
                color = 0

            # send color
            #for i in range(11,89):
            #    self.midiout.send_message([144, i, color])
            #    if i%10 == 3 or i%10 == 6

            i = 11
            for x in range(8):
                for y in range(8):
                    if x in [2,5] or y in [2,5]:
                        self.midiout.send_message([144, i, color+2])
                    else:
                        self.midiout.send_message([144, i, color])

                    i += 1
                i += 2

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

    def sendstate(self):
        """Sends colors and values to MidiFighter"""
        # this contains the colors for the three different states
        # generator : color 0
        # effect 1  : color 40
        # effect 2  : color 80
        # effect 3  : color 120
        color_dict = {0:70, 1:61, 2:50, 3:20}

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

        for i in range(4):
            self.global_parameter[201+i] = self.current_state[i]
