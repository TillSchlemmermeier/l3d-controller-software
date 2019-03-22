import numpy as np
import scipy
from random import randint

class g_inandout:
    def __init__(self):
        self.number = 1
        self.fadespeed = 0.1
        self.leds = []


    def return_values(self):
        pass

    #def generate(self, step, dumpworld):
    def __call__(self, args):
        self.number = int(args[0]*6+1)
        self.fadespeed = 0.5*args[1]+0.01

        tempworld = np.zeros([10, 10, 10])

        # check for new leds
        if len(self.leds) < self.number:
            self.leds.append(led(self.fadespeed))

        delete_index = -1
        # turn on leds
        for i in range(len(self.leds)):
            temp = self.leds[i]()
            if temp[0] < 2:
                world[:, temp[1], temp[2], temp[3]] = temp[4]
            else:
                delete_index = i

        # check for delete
        if delete_index != -1:
            del self.leds[delete_index]

        return np.clip(world, 0, 1)

class led:
    def __init__(self, fadespeed):
        self.x,self.y,self.z = randint(0,9), randint(2,7), randint(2,7)
        self.fadespeed = fadespeed
        self.brightness = 0
        self.state = 0
        self.dx, self.dy, self.dz = 0, 0, 0

        if randint(0, 1) == 1:
            # figure out direction
            if self.z >= 4:
                self.dz = -1
            else:
                self.dz = 1
        else:
            if self.y >= 4:
                self.dy = -1
            else:
                self.dy = 1


    def __call__(self):

#        print(self.state)
#        print(self.brightness)
#        if self.state == 1:
#            print(self.x, self.y, self.z, self.brightness)

        # perform action
        if self.state == 0:
            self.brightness += self.fadespeed
        elif self.state == 1:
            #self.x += self.dx
            self.y += self.dy
            self.z += self.dz
#            print(self.x, self.y, self.z)

        output = [self.state,
                  np.clip(self.x,0,9),
                  np.clip(self.y,0,9),
                  np.clip(self.z,0,9),
                  np.clip(self.brightness,0,1)]

        # check for state
        if self.state == 0 and self.brightness > 1.0:
            self.state = 1
        elif self.state == 1 and (self.x < 0 or self.x > 9 or self.y < 0 or self.y > 9 or self.z < 0 or self.z > 9):
            self.state = 2

        return output
