import numpy as np
import scipy

class g_inandout:
    def __init__(self):
        self.number = 1
        self.fadespeed = 0.1
        self.leds = []

    def control(self, number, fadespeed, blub):
        self.number = int(number*6+1)
        self.fadespeed = 0.5*fadespeed+0.001

    def label(self):
        return ['number',round(self.number,2),
                'fadespeed',round(self.fadespeed,2),
                'empty','empty'']

    def generate(self, step, world):
        tempworld = np.zeros([10, 10, 10])

        # check for new leds
        if len(self.leds) < self.number:
            self.leds.append(led(self.fadespeed))

        # turn on leds
        for i in range(len(self.leds)):
            temp = self.leds[i]()

            if temp[0] < 2:
                world[:, temp[1], temp[2], temp[3]] = temp[4]
            else:
                delete_index = i

        # check for delete
        del self.leds[delete_index]

        return np.clip(world, 0, 1)

class led:
    def __init__(self, fadespeed):
        self.x,self.y,self.z = randint(1,8), randint(1,8), randint(1,8)
        self.fadespeed = fadespeed
        self.brightness = 0
        self.state = 0

        # figure out direction
        if self.x >= 4:
            self.dx = 1
        else:
            self.dx = -1

        if self.y >= 4:
            self.dy = 1
        else:
            self.dy = -1

        if self.z >= 4:
            self.dz = 1
        else:
            self.dz = -1

    def __call__(self):

        # perform action
        if self.state == 0:
            self.brightness += self.fade
        elif self.state == 1:
            self.x += self.dx
            self.y += self.dy
            self.z += self.dz

        output = [self.state, self.x, self.y, self.y, self.brightness]

        # check for state
        if self.state == 0 and self.brightness > 1.0:
            self.state = 1
        elif self.state == 1 and (self.x < 0 or self.x > 9 or self.y < 0 or self.y > 9 or self.z < 0 or self.z > 9):
            self.state = 2

        return output
