'''
Simple script to test the rendering_engine
'''
import threading
import time
from random import randint
import numpy as np

from rendering_engine import rendering_engine

from global_parameter_module import global_parameter

# midi thread
def Midi():
    while True:
        # write random values into array to simulate midi input
        global_parameter[0] = 1
        global_parameter[1] = 200
        global_parameter[3] = 200
        global_parameter[41] = 200
        #global_parameter[randint(0, len(global_parameter)-1)] = randint(0, 100)
        time.sleep(0.1)

def Main():
    frame_renderer = rendering_engine(log = True)
    while True:
        time.sleep(2)
        frame_renderer.run()



# create threads
midi_thread = threading.Thread(name = 'midi', target = Midi)
main_thread = threading.Thread(name = 'main', target = Main)

# start threads
midi_thread.start()
main_thread.start()
