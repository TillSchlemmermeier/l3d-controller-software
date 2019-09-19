'''
Simple script to test the rendering_engine
'''

import time
from MidiDevice import class_fighter
import multiprocessing as mp

def midi(array):
    '''
    Midi Thread
    '''
    print('Starting midi')
    midifighter = class_fighter(global_parameter)

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


# create threads
midi_thread = mp.Process(target=midi)
main_thread = mp.Process(target=main)

# start threads
midi_thread.start()
main_thread.start()


midi_thread.join()
main_thread.join()
