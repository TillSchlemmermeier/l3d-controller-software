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
            if p.serial_number == '55731323536351C012B2':
                self.arduino = serial.Serial('/dev/ttyACM0', 9600)

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

        # create an dict with avaiable presets and what
        # can be [modified, minimal value, maximal value]
        self.presets = {}
        self.presets[1] = [[10, 0, 1]]
        self.presets[4] = [[10, 0, 1]]



    def load_preset(self, preset_id, channel, filename = 'presets.dat'):
        '''loads preset from file and writes to global array
        this is copied from midi_launchpad!'''

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
            pass


    def run(self):

        while True:
            message = self.arduino.read_until(bytearray('\n', 'utf8'))
            try:
                # parse raw message
                message = message.decode("utf-8")

                message = message.split(':')
                value = int(message[1])

                # first, preset encoders
                if message[0] == '00':
                    if value > self.values[0, 0]:
                        print('next preset channel 1')
                        self.values[0, 0] += 1

                        load_preset(self, self.values[0, 0]%len(self.presets.keys(), 1)


                    elif value < self.values[0, 0]:
                        print('previous preset channel 1')
                        self.values[0, 0] -= 1

                        load_preset(self, self.values[0, 0]%len(self.presets.keys(), 1)

                # the, values
                elif message[0] == '01':
                    value = np.round(np.clip(value/1000, 0, 1),1)
                    if value != self.values[0, 1]:
                        print('new value mod channel 1')
                        self.values[0, 1] = value

            except:
                pass

            # sanitize values
            for i in range(3):
                # cut preset id
                #print('self.values: ', self.values[i, 0])
                self.values[i, 0] = self.values[i, 0] % len(self.presets.keys())
                #print('to ', self.values[i, 0])

            time.sleep(0.01)


#    def modifier()
    # orangesquare
    # modifier: speed

    # s2l_donut
    # torus = radius (1)


if __name__ == '__main__':
    midi = class_arduino_midi(np.zeros(2))
    midi.run()
