
from s2l_4_callback2_module import sounddings

print('go')
test = sounddings()

for i in range(10):
    print('-')
    a = test.returndings()
    #print(a)

'''
import pyaudio
import time
import numpy as np


WIDTH = 2
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

#global data # = [0]

data = [0]

def callback(in_data, frame_count, time_info, status):
    print([*in_data[:]][-1])
    data[0] = [*in_data[:]][-1]
    return (in_data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    # print(stream.in_data)
    print('-', data[0])
    time.sleep(0.1)


stream.stop_stream()
stream.close()

p.terminate()
print('-')
print(data)
'''
