import numpy as np
import matplotlib.pyplot as plt
from pyaudio import PyAudio, paFloat32
from time import sleep

pa = PyAudio()

def callback(in_data, frame_count, time_info, flag):
    if flag:
        print("Playback Error: %i" % flag)
    played_frames = counter
    counter += frame_count
    return signal[played_frames:counter], paContinue

stream = pa.open(format = paFloat32,
                 channels = 1,
                 rate = 44100,
                 output = True,
                 frames_per_buffer = 1024,
                 stream_callback = callback)

while stream.is_active():
    sleep(0.1)

stream.close()
pa.terminate()
