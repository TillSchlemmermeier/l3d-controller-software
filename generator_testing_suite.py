# choose generator here

from generators.g_collision import g_collision
generator = g_collision()

# modules
import numpy as np
from random import random
from progress.bar import Bar
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_leds():
    list_world = []
    for x in range(10):
        for y in range(10):
            for z in range(10):
                list_world.append([x, y, z, 0.2])

    return np.array(list_world)

def convert(world):
    list_world = []
    for x in range(10):
        for y in range(10):
            for z in range(10):
                if world[0, x,y,z] > 0:
                    # print(x,y,z)
                    list_world.append([x, y, z, world[0, x, y, z]])

    return np.array(list_world)

# dry run with random values

dummyworld = np.zeros([3,10,10,10])

print('testing...')

bar = Bar('', min=0, max=100, suffix='%(percent)d%%')
for i in range(100):
    generator.control(random(), random(), random())
    for j in range(100):
        generator.generate(i*j, dummyworld)

    bar.next()

bar.finish()

# generate images

print('generating images...')
a,b,c = random(), random(), random()
print('input values:', np.round([a,b,c], 2))
generator = g_collision()
generator.control(a,b,c)
leds = create_leds()

for i in range(40):
    # open figure
    fig = plt.figure(1)
    ax = Axes3D(fig)
    # generate world and convert
    if i == 0:
        world = generator.generate(i, dummyworld)
    else:
        world += generator.generate(i, dummyworld)

    list_world = convert(world)
    # plot
    ax.scatter(leds[:, 0], leds[:, 1], leds[:, 2], s = leds[:, 3])
    if len(list_world) > 0:
        ax.scatter(list_world[:, 0], list_world[:, 1], list_world[:, 2], c = list_world[:,3])

    plt.show()

    world *= 0.9
    # world = np.clip(world, 0.01, 1.0)
