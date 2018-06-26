import sys
import socket
import struct
from timeit import default_timer as timer

artnet = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

#timeval = struct.pack('ll', 2, 100)
#artnet.setsockopt(socket.SOL_SOCKET,SO_RCVTIMEO, timeval)

artnet.settimeout(0.01)

start = timer()

for i in range(100):
    try:
        data = artnet.recvfrom(560)

        if sys.getsizeof(data[0]) >= 512:
            a = data[0][46]

        print(i,' pass')


    except:
        print(i,' timeout')
        pass



end = timer()

print(end-start)

'''
print('')

#artnet.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, 1)
start = timer()


for i in range(20):
    print(i)
    data = artnet.recv(560)
    if sys.getsizeof(data[0]) >= 512:
        a = data[0][46]

end = timer()

print(end-start)
'''
artnet.close()
