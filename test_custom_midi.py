
import serial
from time import sleep
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for p in ports:
    if p.serial_number == '55731323536351C012B2':
        arduino = serial.Serial('/dev/ttyACM0', 9600)


controller_ids = ['00', '01']

while True:
    message = arduino.read_until(bytearray('\n', 'utf8'))
    try:
        message = message.decode("utf-8")
        print(message)
        message = message.split(':')
        print(message[0] in controller_ids)
        ind = controller_ids.index(message[0])
        print('->', ind, message[1])

    except:
        pass

    sleep(0.01)


'''
class custom_midi:
    def __init__(self):
        name = 'arduino'

        self.midiin, self.portname_in = open_midiinput()
        self.midiout, self.portname_out = open_midioutput()

        # initializes the callback
        self.midiin.set_callback(self.event)



    def event(self, event, data=None):
        """Call gets midi message and calls the mapping routine"""

        message, deltatime = event
        print(message)



test_arduino = custom_midi()
while True:
    sleep(0.1)
'''
