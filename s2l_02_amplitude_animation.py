#!/usr/bin/env python
# -*- charset utf8 -*-

import pyaudio
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation
from time import time
from scipy.signal import gaussian

RATE = 44100
BUFFER = 200

p = pyaudio.PyAudio()

stream = p.open(
    format = pyaudio.paFloat32,
    channels = 1,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = BUFFER
)

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

def get_sample():
    try:
        data = np.mean(np.abs(np.fromstring(
               stream.read(BUFFER), dtype=np.float32)))
    except IOError:
        data = None

    return data


starttime = time()
samples = []
max = 1.0
mean = 0.5
med = 0.5
fulldata = []

for i in range(1000):
    data = get_sample()
    # lets get the maximum value
    if len(samples) > 0:
        max = np.max(samples[-500:])
        mean = np.mean(samples[-500:])
        med = np.median(samples[-500:])

    fulldata.append([time()-starttime, max, mean, med])
    samples.append(data)


# make numpy array
fulldata = np.array(fulldata)
samples = np.array(samples)

# make gaussian for convolution
gauss = gaussian(10, 2)

plt.figure(1)
plt.clf()
plt.subplot(2,1,1)
plt.plot(fulldata[:, 0], samples, label = 'data')
plt.plot(fulldata[:, 0], fulldata[:, 1], label = 'max')
plt.plot(fulldata[:, 0], fulldata[:, 2], label = 'mean')
plt.plot(fulldata[:, 0], fulldata[:, 3], label = 'median')
plt.legend()

plt.subplot(2,1,2)

plt.plot(fulldata[:, 0], np.clip(samples-fulldata[:, 3], 0, 1), label = 'corrected data')
plt.plot(fulldata[:, 0], np.convolve(gauss, np.clip(samples-fulldata[:, 3], 0, 1), mode = 'same'), label = 'smoothed data')
plt.legend()
plt.show()
