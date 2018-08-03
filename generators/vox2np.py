#! /usr/bin/python3.5

import numpy as np
import os
import sys

'''
vox2np

Helper to save .vox frames in a numpy-type array. This
hopefully speeds up the loading of those generators,
which use the old .vox animations
'''


def gen_world_from_file(filename):
    # generates a world matrix from a file
    temp = np.genfromtxt(filename, delimiter=',')
    # remove "a" at the end
    data = temp[:-1]
    world = np.zeros([10, 10, 10])
    for i in range(0, len(data)):
        position = (get_position(i))
        if data[i] > 0:
            world[int(position[0]), int(position[1]), int(position[2])] = data[i]/255.0
    return world


def get_position(i):
    # calculates xyz from position in .vox string
    # add zeros for small numbers
    if i >= 100: position = str(i)
    elif i >= 10: position = '0'+str(i)
    else : position = '00'+str(i)

    if int(position[0]) % 2 == 0:
        if int(position[1]) % 2 == 0:
            x = int(position[2])
        else:
            x = 9 - int(position[2])
        y = int(position[1])
    else:
        if int(position[1]) % 2 == 0:
            x = int(position[2])
        else:
            x = 9 - int(position[2])
        y = 9 - int(position[1])
    z = position[0]
    return x, y, z


def main(folder):
    # create list of all filenames
    voxdata = []

    filelist = []
    for file in os.listdir(folder):
        filelist.append(file)

    # strip the .vox part to sort it
    filelist_shorted = []
    for i in filelist:
        filelist_shorted.append(int(i[:-4]))

    # sort the list
    filelist_shorted.sort()

    # add the .vox again
    filelist = []
    for i in filelist_shorted:
        filelist.append(str(i)+'.vox')

    for file in filelist:
        voxdata.append(gen_world_from_file(folder+file))

    return np.array(voxdata)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3.5 vox2np.py <input folder> <output_name>')
    else:
        vox_array = main(sys.argv[1])
        np.save(sys.argv[2], vox_array)
