
import numpy as np

def convert2d(world2d):
    world2d = np.rot90(world2d, axes = (1,2))

    world = np.zeros([3, 10, 10, 10])
    world[:, :, :, 1] = world2d[:,:, :10] #[:, ::-1, ::1]
    world[:, :, :, 0] = world2d[:,:, 10:20][:, :, ::-1]
    world[:, :, :, 3] = world2d[:,:, 20:30]#[:, :, ::-1]
    world[:, :, :, 2] = world2d[:,:, 30:40][:, :, ::-1]
    world[:, :, :, 4] = world2d[:,:, 40:50] #[:, ::1, :]
    world[:, :, :, 5] = world2d[:,:, 50:][:, :, ::-1]

    return world
