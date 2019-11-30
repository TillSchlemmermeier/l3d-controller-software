import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct

class e_s2l_revis():
    def __init__(self):
        self.amount = 1.0
        # sound2light stuff
        self.rate = 44100
        self.buffer = 2**11
        self.last = 0

        p = pyaudio.PyAudio()

        self.stream = p.open(
            format = pyaudio.paFloat32,
            channels = 1,
            rate = self.rate,
            input = True,
            output = False,
            frames_per_buffer = self.buffer
            )

        self.amount = 0.5
        self.threshold = 0.1
        self.channel = 1

    def control(self, amount, threshold, channel):
        self.amount = amount
        self.threshold = threshold
        self.channel = int(channel*4)

    def label(self):
        return ['amount',round(self.amount,2),
                'threshold',round(self.threshold,2),
                'channel',round(self.channel)]

    def generate(self, step, world):
        total_volume = self.update_line()

        world *= total_volume # *self.amount

        return np.clip(world, 0, 1)

    def update_line(self):
        try:
            data = np.fft.rfft(np.fromstring(
                self.stream.read(self.buffer), dtype=np.float32)
            )

            volume = np.mean(np.abs(data)[int(len(data)/2):])

        except IOError:
            pass

        return np.clip(volume-self.threshold, 0, 1E3)
