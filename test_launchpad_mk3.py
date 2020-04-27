import time
from rtmidi.midiutil import open_midiinput,open_midioutput, open_midiport
import numpy as np

class class_launchpad:
    def __init__(self, array):
        # open midi input
        self.midiin, self.portname_in = open_midiinput(port = '20:1')
        self.midiout, self.portname_out = open_midioutput(port = '20:1')
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


array = np.zeros(255)
launchpad = class_launchpad(array)

while True:
    time.sleep(1)
    pass
