import os
import sys
import numpy as np
import pyaudio
import socket
import json
import multiprocessing as mp
from scipy.fftpack import fft, fftfreq
from scipy.ndimage.filters import uniform_filter1d
from time import time, sleep
import struct

def sound_process(state):
    
    # initialize pyaudio
    sample_rate = 44100
    buffer_size = int(44100/20)

    # Suppress stderr output from PyAudio initialization
    devnull = os.open(os.devnull, os.O_WRONLY) # open /dev/null
    original_stderr_fd = os.dup(sys.stderr.fileno()) # Save original stderr fd
    os.dup2(devnull, sys.stderr.fileno()) # Redirect stderr to /dev/null
    p = pyaudio.PyAudio() # Initialize PyAudio
    os.dup2(original_stderr_fd, sys.stderr.fileno()) # Restore original stderr fd
    os.close(original_stderr_fd) # Close the duplicated fd
    os.close(devnull) # Close /dev/null fd

    sound_values = mp.shared_memory.SharedMemory(name = "global_s2l_memory")

    # find pipewire audio device (Nachfolger von pulseaudio)
    pulse_device_index = -1
    for x in range(0,p.get_device_count()):
        info = p.get_device_info_by_index(x)
        if info["name"] == "pipewire":
            pulse_device_index = info["index"]
            print("chosen audio device: ")
            print(info)

    if pulse_device_index == -1:
        print("\nWarning: No pipewire device found, using default input device")
        pulse_device_index = p.get_default_input_device_info()['index']
        print("chosen audio device: ")
        print(p.get_device_info_by_index(pulse_device_index))


    stream = p.open(
        format = pyaudio.paInt16,
        channels = 1,
        rate = sample_rate,
        input_device_index = pulse_device_index,
        input = True,
        output = False,
        frames_per_buffer = buffer_size)

    # initialize frequency axis for spectrum
    freq_axis = np.logspace(0, 5, 60)

    # initialize frequency selector
    selectors = [200, 1000, 2000, 5000] # frequency
    thresholds = [0.0, 0.0, 0.0, 0.0]   # threshold

    print('\nstarting sound loop\n')

    # normalization
    normalized = [False]
    buffer = []
    min = [np.zeros(60)]
    max = [np.ones(60)]

    # trigger
    norm_value = 0.0
    last_value = 0.0
    armed = True
    starttime = time()

    # create LFOs

    lfo = [0.0, 0.0, 0.0, 0.0]

    # === SETUP UDP SOCKET ===
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_dest = ("127.0.0.1", 8001)


    def update():
        '''
        function for update the plotting window, which also
        calls the functions to read the spectrum and parse it

        this function uses `array`, which is passed from the parent
        function to the function `sound_process`. that's the
        global parameters array
        '''
        nonlocal norm_value
        nonlocal last_value
        nonlocal armed
        nonlocal starttime

        if state['s2l_update']:
            # update selectors
            selectors[0] = (state['s2l_values'][0]**2)*10000
            selectors[1] = (state['s2l_values'][1]**2)*10000
            selectors[2] = (state['s2l_values'][2]**2)*10000
            selectors[3] = (state['s2l_values'][3]**2)*10000

            # update threshold
            thresholds[0] = state['s2l_thresholds'][0]
            thresholds[1] = state['s2l_thresholds'][1]
            thresholds[2] = state['s2l_thresholds'][2]
            thresholds[3] = state['s2l_thresholds'][3]
            with state.lock:
                state['s2l_update'] = False

        # check for normalizing
        if state['s2l_normalize']:
            normalized[0] = False
            state['s2l_normalize'] = False
            buffer[:] = []
            print('s2l engine : reseting normalization')

        # read raw data and unpack it
        dump = stream.read(buffer_size)

        # unpack from byte to numbers
        data = np.frombuffer(dump, dtype=np.int16)

        # perform fourier transformation
        FFT   = fft(data)
        freqs = fftfreq(buffer_size, 1.0/sample_rate)

        # smoothing and interpolating to correct axis
        FFT_smooth = uniform_filter1d(np.abs(FFT), size=10)
        # 1-D interpolation onto the log frequency axis
        pos = freqs >= 0
        final_data = np.interp(freq_axis, freqs[pos], FFT_smooth[pos], right=0)

        # normalize the whole thing if normalizing was set
        # to "not normalized"
        if not normalized[0]:
            buffer.append(final_data)

            if len(buffer) > 60:
                print('normalized')
                normalized[0] = True
                min[0] = np.min(np.array(buffer), axis = 0)
                max[0] = np.max(np.array(buffer), axis = 0)

        # final data is the final processed spectrum
        final_data = (final_data - min[0])/(max[0] - min[0] + 0.001)
        
        current_volumes = []

        for i in range(len(selectors)):
            # get data for this frequency
            freq_ind = np.argmin(abs(freq_axis - selectors[i]))
            current_volume = round(final_data[freq_ind],4)

            # apply threshold
            if current_volume < thresholds[0]:
                current_volume = 0.0

            # apply gain
            current_volume *= (state['s2l_gain']*4 + 1)

            current_volumes.append(current_volume)

            # process trigger (only for the first frequency)
            if i == 0:
                trigger_detected = 0.0
                # if loud enough and armed is true, we detect a trigger
                if current_volume > 0.5 and armed:
                    trigger_detected = 1.0
                    armed = False
                    starttime = time()
                elif current_volume < 0.5 and not armed and time()-starttime > 0.3:
                    armed = True
                else:
                    pass

                # read from shared memory to get eventual changes from oneshot
                last_value = struct.unpack('d', sound_values.buf[32:40])[0]
                last_value += trigger_detected

        # Add trigger values
        current_volumes.append(last_value)

        # Add trigger2 values
        if last_value % 2 == 0:
            current_volumes.append(last_value)
        else:
            current_volumes.append(last_value - 1)

        # write the processed sound value for this frequency to shared memory
        sound_values.buf[0:48] = struct.pack('6d', *current_volumes)

        # send data to frontend
        data = {
            "type": "spectrum_data",
            "data": final_data.tolist()
        }

        udp_sock.sendto(json.dumps(data).encode('utf-8'), udp_dest)

    while True:
        update()
        sleep(0.01)