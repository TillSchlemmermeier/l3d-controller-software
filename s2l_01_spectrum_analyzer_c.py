#!/usr/bin/env python
# -*- charset utf8 -*-

import pyaudio
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation
import serial
from time import time, sleep
RATE = 44100
BUFFER = 2**10

p = pyaudio.PyAudio()
times = []
length = 3000


stream = p.open(
    format = pyaudio.paFloat32,
    channels = 1,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = BUFFER
)

fig = plt.figure()
line1 = plt.plot([],[])[0]
line2 = plt.plot([],[])[0]

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

def init_line():
        line1.set_data(r, [-1000]*l)
        line2.set_data(r, [-1000]*l)
        return (line1,line2,)

def update_line(i):

            stream.read(BUFFER), dtype=np.float32)
    )
    data = np.log10(np.sqrt(
        np.real(data)**2+np.imag(data)**2) / BUFFER) * 10

    line1.set_data(r, data)
    line2.set_data(np.maximum(line1.get_data(), line2.get_data()))


#    data = np.random.random(1000)


    # send list to arduino
    # value = np.mean(data)
    send_list = [int(66), int(69), int(69), int(70),*[int(i%2)*50]*(length)]

    # print(send_list)

    # send_list[10] = 255
    package = bytearray(send_list)
    sleep(0.035) # 0.025
    start = time()
    # con.write(package)
    times.append((time() - start)*1E-3)

    return (line1,line2,)
#        send_list.append(int(self.hSpeed))    # SPEED
#        send_list.append(int(self.hBright))   # BRIGHT
#        send_list.append(int(self.hPalMode))  # PalMODE
#        send_list.append(int(self.hPal))      # Pal Select
#        send_list.append(int(self.hRGBMode))  # RGB Mode ON
plt.xlim(0, RATE/2+1)
plt.ylim(-60, 0)
plt.xlabel('Frequency')
plt.ylabel('dB')
plt.title('Spectrometer')
plt.grid()

#Arduino CONECTION
try:
    con =  serial.Serial('/dev/ttyACM0', 230400, write_timeout = 0, timeout = 0.01)
#    con =  serial.Serial('serial0', 230400, write_timeout = 0)
    print('-',con)

except IOError: #, writeTimeout = 0
    con = serial.Serial('/dev/ttyACM1', 230400, write_timeout = 0, timeout = 0.01)
    print(con)

# send list to arduino
send_list = [int(66), int(69), int(69), int(70), *[0]*(length)]
package = bytearray(send_list)
con.write(package)

line_ani = matplotlib.animation.FuncAnimation(
    fig, update_line, init_func=init_line, interval=0, blit=True
)

plt.show()

print()
print(' Mean:   ',np.mean(times), 'ms')
print(' Length: ',length)
print()

plt.figure()
plt.ylabel('ms')
plt.semilogy(times)
plt.show()
