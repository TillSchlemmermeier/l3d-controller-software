#! /usr/bin/python3.5

import numpy as np
import matplotlib.pyplot as plt
import g_collection as g_collection
from random import random
from timeit import default_timer as timer
import sys

list_of_generators = ['g_corner_grow', 'g_growing_sphere',
 #                     'g_planes', 'g_shooting_star',
 #                     'g_corner', 'g_orbiter', 'g_randomlines',
 #                     'g_snake', 'g_cube',
                      'g_planes_falling', 'g_random', 'g_sphere']

runs = int(sys.argv[1])
frames = int(sys.argv[2])

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
