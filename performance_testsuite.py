#! /usr/bin/python3.5

import numpy as np
import matplotlib.pyplot as plt
import g_collection as g_collection
from random import random
from timeit import default_timer as timer
import sys


def main(runs, frames):

    list_of_generators = ['fortran_test_sphere' , 'g_sphere']
      #'g_corner_grow', 'g_growing_sphere',
                          #'g_planes', 'g_shooting_star',
                          #'g_corner', 'g_orbiter', 'g_randomlines',
#                          'g_snake', 'g_cube', 'fortran_test_sphere',
#                          'g_planes_falling', 'g_random', 'g_sphere']
    print('')
    print('------------------------------------------')
    print('Starting test run to study the performance')
    print('------------------------------------------')
    print('')

    for generator in list_of_generators:
        # wierd construction so that I can call the generators by a string
        temp = getattr(g_collection, generator)
        generator_func = temp()

        times = []
     
        for i in range(runs):
            # create random input parameters
            generator_func.control(random(), random(), random())
     	
            start = timer()
     
            for j in range(1, frames):
                dump = generator_func.generate(j, 1.0)
         
            end = timer()
         
            times.append((end-start)/frames)
         
        print('Time used by '+generator+' per frame in milliseconds:')
        print(round(10**(3)*np.mean(times), 4))
        print('')



if len(sys.argv) == 1:
    print("Usage: python performance_testsuite.py <nruns> <nframes>")
else:
    runs = int(sys.argv[1])
    frames = int(sys.argv[2])
    main(runs, frames)


