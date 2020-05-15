import socket
from time import sleep
import numpy as np
import struct

class class_artnet:

    def __init__(self, array):
        # open socket
        self.port = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

        # initialize everything
        self.port.settimeout(0.01)
        self.artnet_universe = np.zeros(255)
        self.global_parameters = array

    def run(self):

        try:
            temp = self.port.recvfrom(560)[0]
            data = [x for x in temp]

            for i in range(255):
                self.artnet_universe[i] = data[46+i]
#                print(self.artnet_universe[0], self.artnet_universe[1], self.artnet_universe[20], self.artnet_universe[40], self.artnet_universe[41])
        except:
#            print('timeout')
            pass

        for i in range(0, 5):
            self.global_parameters[i] = self.artnet_universe[i]/255.0

        for i in range(20, 40):
            self.global_parameters[i] = self.artnet_universe[i]

        for i in range(40, 70):
            self.global_parameters[i] = self.artnet_universe[i]/255.0

'''
# testing script
test = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
test.settimeout(1.0)
#test.artnet_universe = np.zeros(255)

while True:
    a = test.recvfrom(560)[0]
    data = [x for x in a]

    print(data[46:57])
    print(len(data[46:]))
    sleep(0.05)

a = class_artnet()

while True:
    a.run()
    sleep(0.01)
'''
