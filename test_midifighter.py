'''
Simple script to test the rendering_engine
'''

import time
from MidiDevice import class_fighter
import multiprocessing as mp
import numpy as np

def midi(array):
    '''
    Midi Thread
    '''
    print('Starting midi')
    midifighter = class_fighter(array)

    while True:
        time.sleep(1)
        pass

def main(global_parameter):
    '''
    rendering thread
    '''
    # start rendering engine
    while True:
        # long sleeping time, so logfile is not flooded
        time.sleep(2)
        print('1 :: Generator: ', global_parameter[45:49])
        print('1 :: Effect 1 : ', global_parameter[50:54])
        print('1 :: Effect 2 : ', global_parameter[55:59])
        print('1 :: Effect 3 : ', global_parameter[65:69])


global_array = mp.Array('d', [0 for x in range(255)])
print(global_array[:])

# create threads
midi_thread = mp.Process(target=midi, args = [global_array])
main_thread = mp.Process(target=main, args = [global_array])

# start threads
midi_thread.start()
main_thread.start()


midi_thread.join()
main_thread.join()
