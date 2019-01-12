'''
Simple script to test the rendering_engine
'''
import threading
import time
# import rendering class
from rendering_engine import rendering_engine
# import global variable
from global_parameter_module import global_parameter


def Midi():
    '''
    Midi Thread
    '''
    i = 0
    'Waiting some time to start cube...'
    while True:
        print('Some midi input...')
        if i == 5:
            'Starting cube...'
            # write some values into array to simulate midi input
            global_parameter[0] = 1     # staring cube
            global_parameter[1] = 200   # set brightness
            global_parameter[3] = 200   # set brightness limiter
            global_parameter[40] = 1    # activate channel 1

        if i == 10:
            global_parameter[20] = 1    # select g_random

        i += 1
        time.sleep(1)


def Main():
    '''
    rendering thread
    '''

    # start rendering engine
    frame_renderer = rendering_engine(log=True)
    while True:
        # long sleeping time, so logfile is not flooded
        time.sleep(2)
        # render frame
        frame_renderer.run()

# create threads
midi_thread = threading.Thread(name='midi', target=Midi)
main_thread = threading.Thread(name='main', target=Main)

# start threads
midi_thread.start()
main_thread.start()
