import numpy as np
import os

class g_voxreader():
    def __init__(self):
        # create list of all filenames
        self.voxdata = []
        for file in os.listdir("./voxFiles/obliqueplaneXYZ/"):
            print(file)
            self.voxdata.append(self.gen_world_from_file("./voxFiles/obliqueplaneXYZ/"+file))
            #self.files.append(file)

        self.counter = 0
        self.max = len(self.voxdata)

    def control(self, blub0, blub1, blub2):
        pass

    def label(self):
        return ['empty','empty','empty','empty','empty', 'empty']

    def generate(self, step, dumpworld):
        # create empty world
        world = np.zeros([3, 10, 10, 10])

        # choose correct world according to step
        if self.counter >= self.max:
            self.counter = 0

        # copy world from storate to world
        world[0,:,:,:] = self.voxdata[self.counter]

        # increase counter
        self.counter += 1

        # return world
        return np.clip(world,0,1)

    def gen_world_from_file(self, filename):
        # generates a world matrix from a file
        print(filename)
        temp = np.genfromtxt(filename,delimiter=',')
        # remove "a" at the end
        data = temp[:-1]
        world = np.zeros([10,10,10])
        for i in range(0,len(data)):
            position = (self.get_position(i))
            if data[i] > 0 :
                world[position[0],position[1],position[2]] = data[i]/255.0
        return world

    def get_position(self, i):
    # calculates xyz from position in .vox string

    # add zeros for small numbers
        if i >= 100: position = str(i)
        elif i >= 10: position = '0'+str(i)
        else : position = '00'+str(i)

        if int(position[0])%2 == 0:
            if int(position[1])%2 == 0:
                x = int(position[2])
            else:
                x = 9 - int(position[2])
            y = int(position[1])
        else:
            if int(position[1])%2 == 0:
                x = 9 - int(position[2])
            else:
                x = int(position[2])
            y = 9 - int(position[1])
        z = position[0]

        return x,y,z
