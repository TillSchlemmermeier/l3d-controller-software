'''
Simple script to test the rendering_engine
'''
import multiprocessing as mp
import time
# import rendering class
from rendering_engine import rendering_engine
# import global variable
from global_parameter_module import global_parameter


def midi(global_parameter):
    '''
    Midi Thread
    '''
    i = 0
    print('Waiting some time to start cube...')
    while True:
        if i == 1:
            print('Starting cube...')
            # write some values into array to simulate midi input
            global_parameter[0] = 1     # staring cube
            global_parameter[1] = 200   # set brightness
            global_parameter[3] = 200   # set brightness limiter
            global_parameter[40] = 1    # activate channel 1

        if i == 2:
            print('Start g_random...')
            global_parameter[20] = 1    # select g_random

        i += 1
        time.sleep(1)


def rendering(array, pause_time = 0.03, log = False):
    '''
    Rendering Thread
    '''
    print('...starting rendering thread')

    if log == True:
        print('...is logging')
        # long sleeping time, so logfile is not flooded
        pause_time = 2

    # start rendering engine

    frame_renderer = rendering_engine(array, log)

    while True:
        time.sleep(pause_time)
        # render frame
        frame_renderer.run()


global_parameter = mp.Array('d', [0 for x in range(255)])


proc_midi = mp.Process(target=midi, args = [global_parameter])
proc_renderer = mp.Process(target=rendering, args = [global_parameter])

print('start');
proc_midi.start();
proc_renderer.start()

time.sleep(1)

#print('join')
# proc_midi.join();
#self.proc_renderer.join();
print('done')
