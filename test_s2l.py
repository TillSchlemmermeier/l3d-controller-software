from effects.e_s2l import e_s2l
import numpy as np
from time import time, sleep
import matplotlib.pyplot as plt

world = np.zeros([3, 10, 10, 10])

effect = e_s2l()

times = []
times.append(time())

for i in range(40):
    world = effect(world, [0.5, 0.5, 0.5, 0.5])
    times.append(time())
    sleep(0.001)

for i in range(40):
    world = effect(world, [0.5, 0.5, 0.5, 0.5])
    times.append(time())
    sleep(0.01)

for i in range(40):
    world = effect(world, [0.5, 0.5, 0.5, 0.5])
    times.append(time())
    sleep(0.04)

realtimes = []
for i in range(1,3*40):
    realtimes.append(times[i]-times[i-1])

#print(np.round(np.array(times)),4)

plt.figure()
plt.plot(realtimes, 'o-')
plt.show()
