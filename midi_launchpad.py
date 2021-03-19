import time as time
from rtmidi.midiutil import open_midiinput,open_midioutput, open_midiport
from random import randint, random

class class_launchpad_mk3:

    def __init__(self, array):
        # open midi input
        self.midiin, self.portname_in = open_midiinput(port= ':1')
        self.midiout, self.portname_out = open_midioutput(port = ':1')
        self.global_parameter = array
        # activate programming mode
        self.midiout.send_message([240,0,32,41,2,13,14,1,247])
        # turn leds off
        for i, c in zip(range(11,88), range(0,88-11)):
            self.midiout.send_message([144, i, c/1])

        # set callback
        self.midiin.set_callback(self.event)
        # array for state switching
        # states are preset, generator, effect1, effect2, effect3 for
        # each channel, which makes 20 states + idle state
        # state 21 = global preset menu
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

                # start/stop cube
                if message[1] == 88:
                    if self.global_parameter[0] == 1:
                        self.global_parameter[0] = 0
                    else:
                        self.global_parameter[0] = 1
                        self.global_parameter[1] = 1
                        self.global_parameter[2] = 0.0
                        self.global_parameter[3] = 1.0
                        # self.global_parameter[20] = 1
                        # activate channel 1
                        self.global_parameter[40] = 1
                        self.global_parameter[41] = 1
                        # activate channel 2
                        self.global_parameter[70] = 1

                elif message[1] == 18:
                    if self.global_parameter[5] == 0:
                        self.global_parameter[5] = 1
                    else:
                        self.global_parameter[5] = 0


                # check whether button is in range for menus
                if key[0] <= 5 and key[1] <= 4:
                    self.state = key

                    # now we have to send the current state to
                    # global variable
                    # send to global parameter array which menu is open
                    # we can hardcode this for testing

                    # check for channel
                    # write menu to be openend to global parameter
                    # array for gui and so on
                    if key[1]-1 == 0:
                        self.global_parameter[200] = key[0]
                    elif key[1]-1 == 1:
                        self.global_parameter[200] = key[0]+5
                    elif key[1]-1 == 2:
                        self.global_parameter[200] = key[0]+10
                    elif key[1]-1 == 3:
                        self.global_parameter[200] = key[0]+15
                    #elif key[1]-1 == 4:
                    #    self.global_parameter[200] = key

                elif message[1] == 85:
                    self.state = key
                    self.global_parameter[200] = 21

                elif message[1] == 65:
                    self.state = key
                    self.global_parameter[200] = 22

                elif message[1] == 55:
                    self.state = key
                    self.global_parameter[200] = 23

                elif message[1] == 45:
                    self.state = key
                    self.global_parameter[200] = 24

                elif message[1] == 17:
                    self.global_parameter[230] = 1
                    #self.global_parameter[201] = 4
                    #self.global_parameter[202] = 4
                    #self.global_parameter[203] = 4
                    #self.global_parameter[204] = 5

                elif key[0] == 8 and key[1] <= 4:
                    print('saving preset for channel', key[1])
                    try:
                        self.save_preset(key[1])
                    except:
                        print('error saving preset!')

                elif key[0] == 7 and key[1] <= 4:
                    print('saving temporary preset for channel', key[1])
                    try:
                        self.save_preset(key[1], filename = 'temporary_preset.dat')
                    except:
                        print('error saving preset!')

                elif key[0] == 6 and key[1] <= 4:
                    print('loading temporary preset for channel', key[1])
                    try:
                        self.load_preset(-1, key[1], 'temporary_preset.dat')
                    except:
                        print('error loading temporary preset!')

                # now the shots
                elif message[1] == 68:
                    self.global_parameter[220] = 1
                elif message[1] == 67:
                    self.global_parameter[220] = 2
                elif message[1] == 66:
                    self.global_parameter[220] = 3

                elif message[1] == 58:
                    self.global_parameter[220] = 4
                elif message[1] == 57:
                    self.global_parameter[220] = 5
                elif message[1] == 56:
                    self.global_parameter[220] = 6

                elif message[1] == 48:
                    self.global_parameter[220] = 7
                elif message[1] == 47:
                    self.global_parameter[220] = 8

                # now global preset
                elif message[1] == 15:
                    print('saving global preset')
                    self.save_global_preset()

                # now the randomizer
                elif message[1] == 16:
                    self.randomizer()

            else:
                # some selection menu is open

                # self.state[0] ist reihe
                # self.state[1] ist spalte
                if message[1] == 81:
                    self.state = 0
                    self.global_parameter[200] = 0

                else:
                    # check for presets
                    if self.state[0] == 1 and self.state[1] == 5:
                        # figure out the state
                        index = 18 + (self.state[1]-1)*5 + self.state[0]

                        # addition
                        add = -82 + (8-int(message[1]*0.1))*18

                        try:
                            self.load_global_preset(preset_id = message[1]+add)
                        except:
                            print('error loading preset')

                    elif self.state[0] == 1 and self.state[1] < 6:
                        print('trying to load preset')
                        # figure out the state
                        index = 18 + (self.state[1]-1)*5 + self.state[0]

                        # addition
                        add = -82 + (8-int(message[1]*0.1))*18

                        try:
                            self.load_preset(preset_id = message[1]+add, channel = self.state[1])
                        except:
                            print('error loading preset')
                    else:
                        # index is the place to write in the global array
                        # figure out the state
                        index = 18 + (self.state[1]-1)*5 + self.state[0]
                        # print('->', self.state, index)

                        # capture global effect
                        if index == 41:
                            # modify it to 23x
                            index += 190
                        elif index == 42:
                            index += 190
                        elif index == 43:
                            index += 190

                        # print('  ', index)
                        # addition
                        add = -82 + (8-int(message[1]*0.1))*18

                        # print('doing something:', index, add, message[1])

                        self.global_parameter[index] = message[1]+add
                        #print('launchpad sets: ', index, self.global_parameter[index])

        # send colors and state at the end
        self.sendstate()

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

    def save_global_preset(self, filename = 'global_presets.dat'):
        '''appends the current values of a channel to a file
        channel goes from 1 to 4
        '''
        # assemble list of parameters
        list = []
        list.append('name')

        for i in range(20,159):
            list.append(str(round(self.global_parameter[i], 2)))

        for i in range(231,246):
            list.append(str(round(self.global_parameter[i], 2)))
        # save global preset
        with open(filename, 'a+') as file:
            file.write(' '.join(list)+'\n')

    def load_preset(self, preset_id, channel, filename = 'presets.dat'):
        '''loads preset from file and writes to global array'''

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

    def load_global_preset(self, preset_id, filename = 'global_presets.dat'):
        '''loads preset from file and writes to global array'''

        with open(filename, 'r') as file:
            presets = file.readlines()

        try:
            preset = presets[preset_id].strip('\n').split()
            print('loading global preset', preset[0])

            for i, value in zip(range(20,159), preset[1:]):
                self.global_parameter[i] = float(value)

            for i, value in zip(range(231,246), preset[140:]):
                self.global_parameter[i] = float(value)
        except:
            print('global preset not available')


    def convert(self, number):
        """
        converts numbers to correct range
        this is not used at the moment...
        """
        correction = int(number/8)*8 / 2.0
        return number - correction

    def randomizer(self):

        # generator and effect choice
        for i in range(20,40):
            self.global_parameter[i] = randint(0, 54)

        # channels
        for i in [40, 70, 100, 130]:
            self.global_parameter[i] = 0
            for j in range(i+5, i+30):
                self.global_parameter[j] = random()

        # turn channel 1 on
        self.global_parameter[40] = 1


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

        # first, turn all leds off
        for i in range(11,89):
            self.midiout.send_message([144, i, 0])

        # send the state of the channel switches (on/off)
        self.midiout.send_message([176, 91, self.global_parameter[ 40]*127])
        self.midiout.send_message([176, 92, self.global_parameter[ 70]*127])
        self.midiout.send_message([176, 93, self.global_parameter[100]*127])
        self.midiout.send_message([176, 94, self.global_parameter[130]*127])

        # if idle state, we can open the selection menu
        if self.state == 0:
            # send shots
            self.midiout.send_message([144, 68, 5])
            self.midiout.send_message([144, 67, 5])
            self.midiout.send_message([144, 66, 5])
            self.midiout.send_message([144, 58, 5])
            self.midiout.send_message([144, 57, 5])
            self.midiout.send_message([144, 56, 5])
            self.midiout.send_message([144, 48, 5])
            self.midiout.send_message([144, 47, 5])

            # send global preset save/load
            self.midiout.send_message([144, 85, 5])
            self.midiout.send_message([144, 15, 2])

            # send global effect buttons
            self.midiout.send_message([144, 65, 13])
            self.midiout.send_message([144, 55, 21])
            self.midiout.send_message([144, 45, 37])

            # send randomizer
            self.midiout.send_message([144, 16, 23])

            # send global effect control switch for fighter
            self.midiout.send_message([144, 17, 13])

            # send autopilot
            self.midiout.send_message([144, 18, 1])

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
