
'''
Testbed for beat detection / sound to light

Takes some input from audio card (can be the monitor of an output), takes the
FFT and plots the signal levels of the lows, mids and heights.

Maybe only running on Linux, check your pulse audio mixer after
you started the code for a recording device

inspired by
from https://gist.github.com/netom/8221b3588158021704d5891a4f9c0edd
'''
import pyaudio
import numpy
import math
from matplotlib.pyplot import *

# Stuff which i don't fully understand starts here
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

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

def update_line(i):
    try:
        # take FFT of data from buffer
        # buffer size is a critical parameter, i think
        data = numpy.fft.rfft(numpy.fromstring(
            stream.read(BUFFER), dtype=numpy.float32)
        )
    except IOError:
        pass
    data = numpy.log10(numpy.sqrt(
        numpy.real(data)**2+numpy.imag(data)**2) / BUFFER) * 10

    return data

# Stuff which i don't fully understand ends here

data = []       # spectra
nsample = 400   # how many samples to take for demonstration
for i in range(nsample):
    data.append(update_line(i))

# convert to numpy array
data = np.array(data)

# split the spectra and take the mean
# where to split should be fine tuned!
bass_amount = []
mid_amount = []
treble_amount = []

for i in range(nsample):
    bass_amount.append(np.mean(-data[i,10:60]))
    mid_amount.append(np.mean(-data[i,120:250]))
    treble_amount.append(np.mean(-data[i,300:]))

# plotting
figure(1)
subplot(311)
plot(bass_amount)
subplot(312)
plot(mid_amount)
subplot(313)
plot(treble_amount)
show()
