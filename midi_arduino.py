import time as time
import serial
import serial.tools.list_ports
import numpy as np


class class_arduino_midi:

    def __init__(self, array):
        """initializes the MIDI fighter"""

        self.global_parameter = array

        # find correct arduino by serial number
        ports = list(serial.tools.list_ports.comports())

        for p in ports:
            print(p.pid)
            if p.pid == 29987:
                print('found arduino')
                self.arduino = serial.Serial(p.device, 9600)

                print('initialized arduino')

        self.controller_ids = ['00', '01', '10', '11', '20', '21']
        # old values:
        # 1st column value from encoder
        # 2nd column current preset id
        # 3rd column value from modifier
        self.values = np.zeros([3,3])

        # self.inidices is copied from midi_launchpad
        self.indices = []
        self.indices.append([20, 21, 22, 23] + [x for x in range( 40, 70)])
        self.indices.append([25, 26, 27, 28] + [x for x in range( 70,100)])
        self.indices.append([30, 31, 32, 33] + [x for x in range(100,130)])
        self.indices.append([35, 36, 37, 38] + [x for x in range(130,160)])

        # create an list with avaiable presets and what
        # can be [modified, minimal value, maximal value]
        self.presets = []
        self.presets.append([1, [9, 0, 1]])
        self.presets.append([4, [9, 0, 1]])
        self.presets.append([0, [9, 0.16, 1], [10, 0, 0.5]])
        self.presets.append([3, [12, 0, 1]])
        self.presets.append([30, [11, 0, 1]])

    def load_preset(self, preset_id, channel, filename = 'presets.dat'):

        '''loads preset from file and writes to global array
        this is copied from midi_launchpad!'''


        print(preset_id, channel)
        with open(filename, 'r') as file:
            presets = file.readlines()

        try:
            preset = presets[preset_id].strip('\n').split()
            # write values into global parameter array
            # hopefully on the right place
            for i, value in zip(self.indices[channel], preset[1:]):
                # dont set channel on/off
                if i not in [40, 70, 100, 130]:
                    self.global_parameter[i] = float(value)
        except:
            print('ERROR:', preset_id, channel)
            pass


    def run(self):

        while True:
            message = self.arduino.read_until(bytearray('\n', 'utf8'))

            try:
                # parse raw message
                temp = message.decode("utf-8")
                channel = int(temp[0])
                message = int(temp[1])
                value   = int(temp[2:])
                # print('+', channel, message, value)

                # map into self.values
                if message == 0:
                    if value > self.values[0, channel]:
                        self.values[0, channel] = value
                        self.values[1, channel] += 1
                    elif value < self.values[0, channel]:
                        self.values[0, channel] = value
                        self.values[1, channel] -= 1

                    # clip list id to length of preset list
                    self.values[1, channel] = np.clip(self.values[1, channel], 0, len(self.presets)-1)
                    preset_id = self.presets[int(self.values[1, channel])][0]
                    # load preset
                    self.load_preset(int(preset_id), channel)

                elif message == 1:
                    # print('change value')
                    self.values[2, channel] = value/100

                    for mod in self.presets[int(self.values[1, channel])][1:]:
                        temp_val = self.values[2, channel]*(mod[2] - mod[1]) + mod[1]
                        temp_ind = self.indices[channel][mod[0]]
                        self.global_parameter[temp_ind] = temp_val
                        # print(temp_ind,  '->', temp_val)

#                     pos = self.indices[channel][self.preset[self]]



            except:
                pass

            time.sleep(0.01)


#    def modifier()
    # orangesquare
    # modifier: speed

    # s2l_donut
    # torus = radius (1)


if __name__ == '__main__':
    midi = class_arduino_midi(np.zeros(255))
    midi.run()
