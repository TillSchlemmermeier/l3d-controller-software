# modules
import numpy as np
from random import randint, choice
from multiprocessing import shared_memory

class g_randomcross():

    def __init__(self):
        self.number = 2
        self.length = 3
        self.reset = 1
        self.counter = 0
        self.saveworld = np.zeros([3,10,10,10])
        #s2l
        self.sound_values = shared_memory.SharedMemory(name = "global_s2l_memory")
        self.trigger = False
        self.lastvalue = 0

    #Strings for GUI
    def return_values(self):
        return [b'randomcross', b'dimensions', b'length', b'wait', b'Trigger']

    def return_gui_values(self):
        if self.trigger:
            trigger = 'On'
        else:
            trigger = "Off"

        return bytearray('{0:<8s}{1:<8s}{2:<8s}{3:<8s}'.format(str(round(self.number,2)), str(round(self.length,2)), str(round(self.reset,2)), trigger),'utf-8')


    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.number = int(args[0]*2)
        self.length = int(args[1]*10)
        self.reset = int(args[2]*10+1)
        if args[3] > 0.2:
            self.trigger = True
        else:
            self.trigger = False

        world = np.zeros([3, 10, 10, 10])

        #check for trigger
        if self.trigger:
            current_volume = int(float(str(self.sound_values.buf[32:40],'utf-8')))
            if current_volume > self.lastvalue:
                self.lastvalue = current_volume
                self.counter = self.reset
            else:
                self.reset = self.counter + 1


        if self.counter % self.reset == 0:
            xpos = randint(0,9)
            ypos = randint(0,9)
            zpos = randint(0,9)
            number = [0,1,2]

            xmin = xpos-self.length
            if xmin<0: xmin=0
            xmax = xpos+self.length
            if xmax>9: xmax=9
            ymin = ypos-self.length
            if ymin<0: ymin=0
            ymax = ypos+self.length
            if ymax>9: ymax=9
            zmin = zpos-self.length
            if zmin<0: zmin=0
            zmax = zpos+self.length
            if zmax>9: zmax=9

            for x in range(0, self.number+1):
                    direction = choice(number)

                    number.remove(direction)

                    '''
                    if direction == 0:
                        world[:,:,ypos,zpos] = 1
                    elif direction == 1:
                        world[:,xpos,:,zpos] = 1
                    elif direction == 2:
                        world[:,xpos,ypos,:] = 1
                    '''
                    if direction == 0:
                        world[:,xmin:xmax+1,ypos,zpos] = 1
                    elif direction == 1:
                        world[:,xpos,ymin:ymax+1,zpos] = 1
                    elif direction == 2:
                        world[:,xpos,ypos,zmin:zmax+1] = 1
        else:
            world = self.saveworld

        if not self.trigger:
            self.counter +=1

        self.saveworld = world

        return np.clip(world, 0, 1)
