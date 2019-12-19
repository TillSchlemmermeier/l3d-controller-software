#!/usr/bin/env python
# -*- charset utf8 -*-

import pyaudio
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation

RATE = 44100
BUFFER = 882

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
line1 = plt.plot([],[])[0]
line2 = plt.plot([],[])[0]

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

def init_line():
        line1.set_data(r, [-1000]*l)
        line2.set_data(r, [-1000]*l)
        return (line1,line2,)

def update_line(i):
    try:
        data = np.fft.rfft(np.frombuffer(
            stream.read(BUFFER), dtype=np.float32)
        )
    except IOError:
        pass
    data = np.log10(np.sqrt(
        np.real(data)**2+np.imag(data)**2) / BUFFER) * 10
    line1.set_data(r, data)
    line2.set_data(np.maximum(line1.get_data(), line2.get_data()))
    return (line1,line2,)

plt.xlim(0, RATE/2+1)
plt.ylim(-60, 0)
plt.xlabel('Frequency')
plt.ylabel('dB')
plt.title('Spectrometer')
plt.grid()

line_ani = matplotlib.animation.FuncAnimation(
    fig, update_line, init_func=init_line, interval=0, blit=True
)

plt.show()
