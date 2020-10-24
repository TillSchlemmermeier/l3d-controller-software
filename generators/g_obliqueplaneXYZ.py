import numpy as np
import os
from multiprocessing import shared_memory

class g_obliqueplaneXYZ():
    def __init__(self):
        # create list of all filenames
        self.voxdata = []

        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.channel = 0

        filelist = []
        for file in os.listdir('./voxFiles/obliqueplaneXYZ/'):
            #self.voxdata.append(self.gen_world_from_file("./voxFiles/obliqueplaneXYZ/"+file))
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
            self.voxdata.append(self.gen_world_from_file('./voxFiles/obliqueplaneXYZ/'+file))

        self.counter = 0
        self.max = len(self.voxdata)
        self.wait = 5
        self.step = 0

    #Strings for GUI
    def return_values(self):
        return [b'obliqueplaneXYZ', b'wait', b'', b'', b'channel']

    def return_gui_values(self):
        if self.channel >=0:
            channel = str(self.channel)
        else:
            channel = 'noS2L'

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.wait,2)), '', '', channel),'utf-8')


    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.wait = int(args[0]*10)+1
        self.channel = int(args[3]*4)-1

        # create empty world
        world = np.zeros([3, 10, 10, 10])

        # choose correct world according to step
        if self.counter >= self.max:
            self.counter = 0

        # copy world from storate to world
        world[0,:,:,:] = self.voxdata[self.counter]
        world[1,:,:,:] = world[0,:,:,:]
        world[2,:,:,:] = world[0,:,:,:]

        # check if S2L is activated
        if self.channel >= 0:
            current_volume = float(str(self.sound_values.buf[self.channel*8:self.channel*8+8],'utf-8'))
            if current_volume > 0.1:
                self.counter += 1
            #current_volume = int(current_volume * 9)
            #if self.step % 4-current_volume == 0:
            #    self.counter += 1

        # increase counter
        else:
            if self.step % self.wait == 0:
                self.counter += 1

        self.step += 1
        # return world
        return np.clip(world,0,1)

    def gen_world_from_file(self, filename):
        # generates a world matrix from a file
        temp = np.genfromtxt(filename,delimiter=',')
        # remove "a" at the end
        data = temp[:-1]
        world = np.zeros([10,10,10])
        for i in range(0,len(data)):
            position = (self.get_position(i))
            if data[i] > 0 :
                world[int(position[0]),int(position[1]),int(position[2])] = data[i]/255.0
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
#                x = 9 - int(position[2])
                x = int(position[2])
            else:
                x = 9 - int(position[2])
            y = 9 - int(position[1])
        z = position[0]

        return x,y,z
