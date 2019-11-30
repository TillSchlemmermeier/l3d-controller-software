#!/usr/bin/env python
# -*- charset utf8 -*-

import pyaudio
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation
import scipy
from scipy.signal import gaussian as Gaussian

RATE = 44100
BUFFER = 882
N = 100

p = pyaudio.PyAudio()

stream = p.open(
    format = pyaudio.paFloat32,
    channels = 1,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = BUFFER
)

fig = plt.figure()
line1 = plt.plot([], [])[0]
line2 = plt.plot([], [])[0]

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

gaussian = Gaussian(21,10)
gaussian[0] = 0.0
gaussian[-1] = 0.0

def init_line():
        line1.set_data(r, [-1000]*l)
        line2.set_data(r, [-1000]*l)
        return (line1,line2,)

def update_line(i):
    try:
        data = np.fft.rfft(np.fromstring(
            stream.read(BUFFER), dtype=np.float32)
        )
    except IOError:
        pass
    data = np.log10(np.sqrt(
        np.real(data)**2+np.imag(data)**2) / BUFFER) * 10

    N = 2
    yy = [ np.mean(data[n:n+N]) for n in range(0, len(data), N)]
    yy = yy[:int(len(yy)/2)] # Discard half of the samples, as they are mirrored


    newr = [x for x in range(len(yy))]

#    print(data[10], yy[10])
#    print(np.shape(data), np.shape(yy))
    #    line1.set_data(yy)
    gdata = np.convolve(data, gaussian, mode = 'same')
#    print(gdata)
#    print(np.shape(data), np.shape(gdata))
    line1.set_data([r, gdata])
#    line1.set_data([newr, yy])
    line2.set_data(np.maximum(line1.get_data(), line2.get_data()))
    return (line1,line2,)

plt.xlim(1, RATE/2)
plt.ylim(-1200, 0)
plt.xlabel('Frequency')
plt.ylabel('dB')
plt.title('Spectrometer')
plt.grid()

line_ani = matplotlib.animation.FuncAnimation(
    fig, update_line, init_func=init_line, interval=0, blit=True
)

plt.show()
