# modules
import numpy as np
from cube_utils import *
from random import uniform, randint
#import Generator.py

# list of Effects:
# osci_planes, growing_sphere, dots_on_pshere, sphere, hsphere, random_lines, random, cube, corner_gen, block
'''
class passing_planes_generator(Generator):
    def __init__(self):
        super().__init__(self)
        self.speed = 0
        self.size = 0
        self.dir = 0
        self.position = 0
    def control(speed,size,direction):
        self.speed = speed
        self.size = size
        self.dir = direction
    def generate(world,step):
        # converting input
        self.speed = int((speed/127.0)*9)
        self.size = int((size/127.0)*4)
        self.dir = int(round((dir/127.0)*5))
        self.position = frame % 10s

        world=new_world(10)
        if self.dir == 0:
            world[position,:,:] = 1.0
        elif self.dir == 1:
            world[9-position, :,:] = 1.0
        elif self.dir == 2:
            world[:, position,:] = 1.0
        elif self.dir == 3:
            world[:, 9-position,:] = 1.0
        elif self.dir == 4:
            world[:, :,position] = 1.0
        elif self.dir == 5:
            world[:, :,9-position] = 1.0

        self.world_R = world
        self.world_G = world
        self.world_B = world
'''

def passing_planes(world, frame, speed, size, dir):
    # converting input
    speed = int((speed/127.0)*9)
    size = int((size/127.0)*4)
    dir = int(round((dir/127.0)*5))

    position = frame % 10

    if dir == 0:
        world[position,:,:] = 1.0
    elif dir == 1:
        world[9-position, :,:] = 1.0
    elif dir == 2:
        world[:, position,:] = 1.0
    elif dir == 3:
        world[:, 9-position,:] = 1.0
    elif dir == 4:
        world[:, :,position] = 1.0
    elif dir == 5:
        world[:, :,9-position] = 1.0

    return world


def osci_planes(world, frame, speed, size, dir):
    # converting input
    speed = int((speed/127.0)*9)
    size = int((size/127.0)*4)
    dir = int(round((dir/127.0)*3))

    position = int( round((np.sin(0.1*frame*speed)+1)*4.5))

    if dir == 0:
        world[position,:,:] = 1.0
    elif dir == 1:
        world[:, position,:] = 1.0
    else:
        world[:,:,position] = 1.0

    return world



def growing_sphere(world, frame, speed, nwait):
    '''
    Grpwing sphere
    '''
    #brightness = brightness/127.0

    # converting input
    size = ((nwait/127.0)+2) * frame%(speed+1)*2
    world = hsphere(world, frame, size, 4.5, 4.5, 4.5, 1.0)
    return np.round(np.clip(world, 0, 1), 3)

def dots_on_sphere(world, frame, number, radius, brightness = 127):
    '''
    Generator: dots_on_sphere

    01  number of led per frames
    02  size of sphere

    creates <number> random dots on a sphere with <radius>
    sphere is centered in the middle
    '''
    # converting input
    number = int(round((number/127.0)*10))

    sphereworld = world_init(10)
    #dotworld = world_init(10)

    sphere_world = sphere(sphereworld, frame, radius, 127/2.0, 127/2.0, 127/2.0, brightness)

    for i in range(number):
        x = randint(0, 9)
        y = randint(0, 9)
        z = randint(0, 9)
        world[x, y, z] = sphere_world[x, y, z]

    return world

def sphere(world, frame, radius, xpos, ypos, zpos, brightness=1.0):
    '''
    Generator: sphere

    01  radius of spheres
    02  x positions
    03  y positions
    04  z positions

    creates a sphere with given parameters, assign oscillator to
    positions!
    '''
    # converting input
    radius = (radius/127.0)*5
    xpos = (xpos/127.0)*9
    ypos = (ypos/127.0)*9
    zpos = (zpos/127.0)*9


    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                dist = np.sqrt((x-xpos)**2+(y-ypos)**2+(z-zpos)**2)
                if dist <= radius:
                    world[x,y,z] = brightness

    return world

def randomsphere(world, frame, radius, brightness=1.0):
    '''
    Generator: sphere

    01  radius of spheres
    02  x positions
    03  y positions
    04  z positions

    creates a sphere with given parameters, assign oscillator to
    positions!
    '''
    # converting input
    radius = (radius/127.0)*5

    xpos = randint(0,9)
    ypos = randint(0,9)
    zpos = randint(0,9)

    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                dist = np.sqrt((x-xpos)**2+(y-ypos)**2+(z-zpos)**2)
                if dist <= radius:
                    world[x,y,z] = brightness

    return world

def hsphere(world,frame, radius,xpos,ypos,zpos,brightness=1.0):
    '''
    Generator: hollow sphere

    01  radius of spheres
    02  x positions
    03  y positions
    04  z positions

    creates a hollow sphere with given parameters, assign oscillator to
    positions!
    '''
    # converting input
    radius = (radius/127.0)*5

    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                dist = np.sqrt((x-xpos)**2+(y-ypos)**2+(z-zpos)**2)
                world[x, y, z] = brightness/(radius-dist+0.0001)**5

    return np.round(np.clip(world, 0, 1), 3)

def random_lines(world, frame):

    direction = randint(0,2)
    if direction == 0:
        world[:, randint(0,9), randint(0,9)] = 1
    elif direction == 1:
        world[randint(0,9), :, randint(0,9)] = 1
    elif direction == 2:
        world[randint(0,9), randint(0,9), :] = 1

    return world


def random_lines_Y(world, frame, length, number):
    '''
    Generator: random lines

    01  length
    02  number
    '''
    # converting input
    length = int(round((length/127.0)*10))
    number = int(round((number/127.0)*5))

    for n in range (number):
        direction = randint(0,2)
        position = randint(0,10-length)
        if direction == 0:
            y = randint(0,9)
            z = randint(0,9)
            for x in range(position,(position+length)):
                world[x, y, z] = 1
        elif direction == 1:
            x = randint(0,9)
            z = randint(0,9)
            for y in range(position,(position+length)):
                world[x, y, z] = 1
        elif direction == 2:
            x = randint(0,9)
            y = randint(0,9)
            for z in range(position,(position+length)):
                world[x, y, z] = 1

    return world



def lines(world, frame):
    '''
    Generator: lines

    creates lines starting at y = 0 or y = 9 depending on the frame
    number and with random x,z positions and random length.
    Works well with effect seperate.
    '''
    x = randint(0, 9)
    z = randint(0, 9)
    length = randint(1, 4)

    if frame % 2 == 0:
        world[x, :length, z] = 1
    else:
        world[x, 9-length:, z] = 1

    return world

def random(world, frame, number):
    '''
    Generator: random

    01  number of leds

    Turns on <number> LEDS at random positions
    '''
    # converting input
    number = int(round((number/127.0)*10))

    for i in range(number):
        x = randint(0, 9)
        y = randint(0, 9)
        z = randint(0, 9)
        world[x, y, z] = 1

    return world

def corner_static(world, frame, size):

    '''
    Generator: random

    02  size

    Turns on LEDS with size at corner positions
    '''
    # converting input
    size = int((size/127.0)*5)

    for x in range (size):
        for y in range (size):
            for z in range (size):
                    world[x, y, z] = 1
                    world[9-x, y, z] = 1
                    world[x, 9-y, z] = 1
                    world[x, y, 9-z] = 1
                    world[9-x, 9-y, z] = 1
                    world[9-x, y, 9-z] = 1
                    world[x, 9-y, 9-z] = 1
                    world[9-x, 9-y, 9-z] = 1

    return world

def corner_random(world, frame, number,size):
    '''
    Generator: random

    01  number of leds in the corner
    02  size

    Turns on <number> LEDS at corner positions
    '''
    # converting input
    number = int((number/127.0)*8)
    size = int((size/127.0)*5)

    for i in range(number):
#        x = randint(0, 1)*9
#        y = randint(0, 1)*9
#        z = randint(0, 1)*9
        case = randint(0,7)
        for x in range (size):
            for y in range (size):
                for z in range (size):
                    if case == 0:
                        world[x, y, z] = 1
                    elif case==1:
                        world[9-x, y, z] = 1
                    elif case==2:
                        world[x, 9-y, z] = 1
                    elif case==3:
                        world[x, y, 9-z] = 1
                    elif case==4:
                        world[9-x, 9-y, z] = 1
                    elif case==5:
                        world[9-x, y, 9-z] = 1
                    elif case==6:
                        world[x, 9-y, 9-z] = 1
                    elif case==7:
                        world[9-x, 9-y, 9-z] = 1

    return world

def cube(world, frame, size):
    '''
    Generator: cube

    01  size of cube

    Generates a cube in the cube!
    '''

    # converting input
    size = (size/127.0)*4

    size = np.ceil(size)
    if size > 4:
        size = 4

    tempworld = world_init(10)
    tempworld[:, :, :] = -1.0
    # x slices
    tempworld[4-round(size), 4-round(size):6+round(size), 4-round(size):6+round(size)] += 1
    tempworld[5+round(size), 4-round(size):6+round(size), 4-round(size):6+round(size)] += 1
    # y slices
    tempworld[4-round(size):6+round(size), 4-round(size), 4-round(size):6+round(size)] += 1
    tempworld[4-round(size):6+round(size), 5+round(size), 4-round(size):6+round(size)] += 1
    # z slices
    tempworld[4-round(size):6+round(size), 4-round(size):6+round(size), 4-round(size)] += 1
    tempworld[4-round(size):6+round(size), 4-round(size):6+round(size), 5+round(size)] += 1

    return np.round(np.clip(world+np.clip(tempworld, 0, 1),0,1),3) # np.round(np.clip(world*fade, 0, 1), 3)

def block(world, frame, sx, sy, sz):

    # converting input
    sx = int(round((sx/128.0) * 8))
    sy = int(round((sy/128.0) * 8))
    sz = int(round((sz/128.0) * 8))

    print(sx,sy,sz)
    # get random position
    x = randint(0,9)
    y = randint(0,9)
    z = randint(0,9)

    # add block to world
    world[x-sx:x+sx+1,y-sy:y+sy+1,z-sz:z+sz+1] += 1.0

    return np.round(np.clip(world, 0, 1), 2)

def block_position(world, frame, sx, sy, sz, px, py, pz):

    # converting input
    sx = int(round((sx/128.0) * 8))
    sy = int(round((sy/128.0) * 8))
    sz = int(round((sz/128.0) * 8))

    world[px-sx:px+sx+1,py-sy:py+sy+1,pz-sz:pz+sz+1] += 1.0

    return np.round(np.clip(world, 0, 1), 2)

# unused


def tempsphere(world, frame, radius, xpos, ypos, zpos, brightness=1.0):
    '''
    Generator: sphere

    01  radius of spheres
    02  x positions
    03  y positions
    04  z positions

    creates a sphere with given parameters, assign oscillator to
    positions!
    '''


    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                dist = np.sqrt((x-xpos)**2+(y-ypos)**2+(z-zpos)**2)
                if dist <= radius:
                    world[x,y,z] = brightness

    return world


def moving_circle(world, frame, speed, size):
    # converting input
    speed = int((speed/127.0)*9)
    size = int((size/127.0)*4)
    frames = []

    # size 4
    frames.append(np.array([
            [1, 1, 4],
            [2, 1, 3],
            [3, 2, 2],
            [4, 3, 1],
            [5, 4, 1],
            [6, 5, 1],
            [7, 6, 1],
            [8, 7, 2],
            [9, 8, 3],
            [0, 8, 4],
            [1, 8, 5],
            [2, 8, 6],
            [3, 7, 7],
            [4, 6, 8],
            [5, 5, 8],
            [6, 4, 8],
            [7, 3, 8],
            [8, 2, 7],
            [9, 1, 6],
            [0, 1, 5]
            ]))

    # size 3
    frames.append(np.array([
            [1, 2, 4],
            [2, 2, 3],
            [3, 3, 2],
            [4, 4, 2],
            [5, 5, 2],
            [6, 6, 2],
            [7, 7, 3],
            [8, 7, 4],
            [9, 7, 5],
            [0, 7, 6],
            [1, 6, 7],
            [2, 5, 7],
            [3, 4, 7],
            [4, 3, 8],
            [5, 2, 6],
            [6, 2, 5]
            ]))

    # size 3
    frames.append(np.array([
            [1, 2, 4],
            [2, 2, 3],
            [3, 3, 2],
            [4, 4, 2],
            [5, 5, 2],
            [6, 6, 2],
            [7, 7, 3],
            [8, 7, 4],
            [9, 7, 5],
            [0, 7, 6],
            [1, 6, 7],
            [2, 5, 7],
            [3, 4, 7],
            [4, 3, 8],
            [5, 2, 6],
            [6, 2, 5]
            ]))

    # size 2
    frames.append(np.array([
            [1, 3, 4],
            [2, 4, 3],
            [3, 5, 3],
            [4, 6, 4],
            [5, 6, 5],
            [6, 5, 6],
            [7, 4, 6],
            [8, 3, 5]
            ]))

#    if type(height) == int:
#        height = [height]

    position = int( (np.sin(0.1*frame*speed)+1)*4.5)

    for i in frames[size]:
        #print('')
        for j in i:
            world[position,:,:] = 1.0

#            world[position,j[1],j[2]] = 1.0

#    world += frame[int(position*len(frame))]

#    for h in height:
#    for i in range(len(frames)):
#        world[height, frames[i, 1], frames[i, 2]] = 1



    return world


def planes(world, frame, vx, vy, vz, j):
    '''
    Generator: planes

    01  x vector
    02  y vector
    03  z vector
    04  origin (?)

    creates a plane at <j>, with directions as given by
    vx, vy, vz. Assign oscillator to these!
    '''

    # converting input
    vx = (vx/127.0 - 255/2)*5
    vy = (vy/127.0 - 255/2)*5
    vz = (vz/127.0 - 255/2)*5
    j = (j/127.0) * 9
    # plane a*x + b*y + c*z = a

    # n = np.sqrt(a**2+b**2+c**2)
    # d = (a*x+b*y+c*z-a)/n

    def distance(plane,a,x,y,z):
        n = np.sqrt(plane[0]**2+plane[1]**2+plane[2]**2)
        return abs((plane[0]*x+plane[1]*y+plane[2]*z-a)/n)

    for x in range(10):
        for y in range(10):
            for z in range(10):
                world[x,y,z] = 1/(2*distance([vx,vy,vz],j,x,y,z))

    return np.round(np.clip(world, 0, 1), 2)

def random_block(world, frame, size_x, size_y, size_z):
    # converting input
    size_x = int((size_x/127.0)*9)
    size_y = int((size_y/127.0)*9)
    size_y = int((size_z/127.0)*9)

    print(size_x, size_y, size_z)
    xpos = randint(0,(10-size_x))
    ypos = randint(0,(10-size_y))
    zpos = randint(0,(10-size_z))


    for x in range (xpos,size_x+xpos):
        for y in range (ypos,size_y+ypos):
            for z in range (zpos,size_z+zpos):
                world[x, y, z] = 1.0

    return world

def random_block_outlines(world, frame, size_x, size_y, size_z):
    # converting input
    size_x = int((size_x/127.0)*9)
    size_y = int((size_y/127.0)*9)
    size_y = int((size_z/127.0)*9)

    xpos = randint(0,(10-size_x))
    ypos = randint(0,(10-size_y))
    zpos = randint(0,(10-size_z))

    # x slices
    world[xpos:xpos+size_x, ypos,               zpos] = 1
    world[xpos:xpos+size_x, ypos+size_y,        zpos] = 1
    world[xpos:xpos+size_x, ypos,               zpos+size_z] = 1
    world[xpos:xpos+size_x, ypos+size_y,        zpos+size_z] = 1
    # y slices
    world[xpos,             ypos:ypos+size_y,   zpos] = 1
    world[xpos+size_x,      ypos:ypos+size_y,   zpos] = 1
    world[xpos,             ypos:ypos+size_y,   zpos+size_z] = 1
    world[xpos+size_x,      ypos:ypos+size_y,   zpos+size_z] = 1
    # z slices
    world[xpos,             ypos,               zpos:zpos+size_z] = 1
    world[xpos+size_x,      ypos,               zpos:zpos+size_z] = 1
    world[xpos,             ypos+size_y,        zpos:zpos+size_z] = 1
    world[xpos+size_x,      ypos+size_y,        zpos:zpos+size_z] = 1

    return world
