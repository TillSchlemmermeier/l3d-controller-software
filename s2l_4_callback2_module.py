
import pyaudio
import time
import numpy as np

def callback(in_data, frame_count, time_info, status):
    # print([*in_data[:]][-1])
    data[0] = [*in_data[:]][-1]
    return (in_data, pyaudio.paContinue)

data = [0]

class sounddings:

    def __init__(self):

        self.WIDTH = 2
        self.CHANNELS = 2
        self.RATE = 44100
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(self.WIDTH),
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                output=True,
                stream_callback=callback)

        stream.start_stream()

        #while stream.is_active():
            # print(stream.in_data)
            # print('-', data[0])
        #    time.sleep(0.1)

        #stream.stop_stream()
        #stream.close()
        #p.terminate()

    def returndings(self):
        pass
