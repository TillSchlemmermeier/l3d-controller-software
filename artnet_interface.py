import socket
from time import sleep

class class_artnet:

    def __init__(self, array):
        # open socket
        self.port = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

        # initialize everything
        self.port.settimeout(0.006)
        self.artnet_universe = np.zeros(255)

# testing script
test = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
test.port.settimeout(0.006)
test.artnet_universe = np.zeros(255)

while True:
    print(test.recvfrom(560))
    sleep(0.1)
