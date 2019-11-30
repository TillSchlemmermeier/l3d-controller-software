import matplotlib.animation as animation
import numpy as np
from random import randint
from matplotlib import pyplot as plt
import time

from generators.g_2d_rain import g_2d_rain
from generators.g_2d_square import g_2d_square
from generators.g_2d_portal import g_2d_portal
from generators.g_2d_randomlines import g_2d_randomlines
from generators.g_2d_growing_circle import g_2d_growing_circle
# from generators.g_2d_random_inner_square import g_2d_random_inner_square
from generators.g_2d_random_squares import g_2d_random_squares
from generators.g_2d_orbiter import g_2d_orbiter
from generators.g_2d_patches import g_2d_patches

#generator = g_2d_square(test = True)
#generator = g_2d_random_squares(test = True)
#generator = g_2d_orbiter(test = True)
generator = g_2d_patches(test = True)

def convert(world):
    list_world = []
    for x in range(60):
        for y in range(10):
            if world[:, x, y].any() > 0.0:
                list_world.append([x, y, world[:, x, y].cumsum()[-1]/3.0])

    return np.array(list_world)

world = np.zeros([3, 60, 10])
world[:, 0, 0] = 1.0
world[0, -1, -1] = 1.0

world_list = convert(world)

'''
plt.figure



plt.scatter(world_list[:, 0], world_list[:, 1], c = world_list[:, 2], cmap='Greys')
'''

fig = plt.figure()
scat = plt.scatter(world_list[:, 0], world_list[:, 1], c=world_list[:, 2], cmap = 'Greys')

# center
plt.plot([0,59], [4.5,4.5], '--', color = 'black')
plt.plot([29.5,29.5], [0,9], '--', color = 'black')

# box
plt.plot([0,0], [0,9], color = 'black')
plt.plot([59,59], [0,9], color = 'black')
plt.plot([0,59], [0,0], color = 'black')
plt.plot([0,59], [9,9], color = 'black')


plt.xlim([-0.5, 59.5])
plt.ylim(-0.5, 9.5)


def animate(i, world, scat):

#    time.sleep(0.5)

    world *= 0.5
    world += generator.generate(i, world)
    list_world = convert(world)
    scat.set_offsets(list_world[:, :2])
    scat.set_array(list_world[:, 2])
    return scat,

ani = animation.FuncAnimation(fig, animate, 100,
                              fargs=(world, scat))
plt.show()
