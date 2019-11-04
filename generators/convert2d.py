
import numpy as np

def convert2d(world2d):
    world = np.zeros([3, 10, 10, 10])
    world[:, :, :, 1] = world2d[:, :10, :10][:, ::-1, ::1]
    world[:, :, :, 0] = world2d[:, :10, 10:20][:, ::-1, ::-1]
    world[:, :, :, 2] = world2d[:, :10, 20:30][:, ::-1, ::1]
    world[:, :, :, 3] = world2d[:, :10, 30:40][:, ::-1, ::-1]
    world[:, :, :, 4] = world2d[:, 10:, 10:20][:, ::1, :]
    world[:, :, :, 5] = world2d[:, 10:, 20:30][:, ::1, ::-1]

    return world
