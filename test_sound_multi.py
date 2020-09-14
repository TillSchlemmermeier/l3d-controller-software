import numpy as np
import pyaudio
from scipy.fftpack import fft, fftfreq
import scipy
import struct
from time import sleep
import multiprocessing as mp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import griddata
from scipy.ndimage.filters import uniform_filter1d

def sound_monitor():
    sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
    while True:
        print(sound_values)
        sleep(1)


def midi_sim(array):
    i = 100
    while True:
        array[10] = i
        array[11] = 500
        array[12] = 2000
        i += 100
        print(array[10], array[11], array[12])
        sleep(2)


def sound_process(array):
    # initialize pyaudio
    sample_rate = 44100
    buffer_size = int(44100/20)
    p = pyaudio.PyAudio()
    sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")

    stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = sample_rate,
        input = True,
        output = False,
        frames_per_buffer = buffer_size)

    freq_axis = 10000*np.linspace(0, 1, 40)**2

    # initialize selector
    selectors = [1000, 3000, 7000, 9000]
    # inital read
    dump = stream.read(1024)
    data = struct.unpack("%dh"%(1024), dump)
    FFT = fft(data)
    freqs = fftfreq(1024, 1.0/sample_rate)

    print('\nstarting sound loop\n')

    # initialize figure
    fig, ax = plt.subplots()
    ax.set_xlim(50, 10000)
    ax.set_ylim(-0.1,2)
    line = ax.plot(freqs, np.abs(FFT))[0]
    select1 = ax.axvline(selectors[0], label = '1', color = 'red')
    select2 = ax.axvline(selectors[1], label = '2', color = 'green')
    select3 = ax.axvline(selectors[2], label = '3', color = 'orange')
    select4 = ax.axvline(selectors[3], label = '4', color = 'violet')
    ax.set_xscale('symlog', linthreshx=0.01)

    ax.set_xticks([50, 100, 250, 500, 1000, 2500, 5000, 10000])
    ax.set_xticklabels([50, 100, 250, 500, 1000, 2500, 5000, 10000])
    plt.legend()

    # normalization
    normalized = [False]
    buffer = []
    min = [np.zeros(40)]
    max = [np.ones(40)]

    def update_line(frame, normalized, buffer, min, max):
        # update selectors
        selectors[0] = array[10]*10000
        selectors[1] = array[11]*10000
        selectors[2] = array[12]*10000
        selectors[3] = array[13]*10000

        # read raw data and unpack it
        n_available = stream.get_read_available()
        dump = stream.read(buffer_size)
        data = struct.unpack("%dh"%(buffer_size), dump)

        # perform fourier transformation
        FFT = fft(data)
        freqs = fftfreq(buffer_size, 1.0/sample_rate)

        # smoothing and interpolating to correct axis
        FFT_smooth = uniform_filter1d(np.abs(FFT), size=10)
        final_data = griddata(freqs, FFT_smooth, freq_axis, method='cubic', fill_value=0)

        # normalize the whole thing
        if not normalized[0]:
            buffer.append(final_data)

            if len(buffer) > 50:
                print('normalized')
                normalized[0] = True
                min[0] = np.min(np.array(buffer), axis = 0)
                max[0] = np.max(np.array(buffer), axis = 0)


        final_data = (final_data - min[0])/(max[0] - min[0])

        # set data
        line.set_data(freq_axis, final_data)
        select1.set_data(selectors[0])
        select2.set_data(selectors[1])
        select3.set_data(selectors[1])
        select4.set_data(selectors[1])

        # write data
        for i in range(len(selectors)):
            freq_ind = np.argmin(abs(freq_axis - selectors[i]))
            sound_values[i] = final_data[freq_ind]


        print('->', sound_values)
        return line,

    animation = FuncAnimation(fig, func = update_line, interval=0.001, blit=True, fargs = (normalized, buffer, min, max))
    plt.show()

if __name__ == '__main__':
    # initialize sound shared memory
    global_memory = mp.shared_memory.SharedMemory(create = True, name = "global_s2l_memory", size = 10)
    global_parameter = mp.Array('d', [0 for x in range(255)])

    # init processes
    proc_reader = mp.Process(target = sound_monitor)
    proc_writer = mp.Process(target = sound_process, , args = [global_parameter])
    proc_midi = mp.Process(target = midi_sim, , args = [global_parameter])

    # starting processes
    print('start')
    proc_reader.start()
    proc_writer.start()
    proc_midi.start()
    
