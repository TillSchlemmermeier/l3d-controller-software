'''
Simple script to test the rendering_engine
'''
import threading
import time
from MidiDevice import class_fighter
# import global variable
from global_parameter_module import global_parameter


def midi():
    '''
    Midi Thread
    '''
    print('Starting midi')
    midifighter = class_fighter(in_port = 2,out_port = 2)



def main():
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
midi_thread = threading.Thread(name='midi', target=midi)
main_thread = threading.Thread(name='main', target=main)

# start threads
midi_thread.start()
main_thread.start()
