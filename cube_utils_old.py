
'''

Routines for crazy led stuff

content:

1. Basic routines
   - world_init
   - move_z
   - transform   (world->plot)
   - transform_2 (world->.vox)
   - gen_world_from_file
   - get_position

2. Spawning routines/ creating shapes
   - world_random
   - spawn_sphere
   - spawn_hollow_sphere
   - spawn_fading_line

3. Conway stuff
   - number_of_neighbours
   - evolve

4. Visualization
   - visualize

'''
import numpy as np
import scipy as sp

from scipy.ndimage import gaussian_filter
from random import randint,seed
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

# ------------------------------------------
# 1. basic routines

def world_init(dim):
    # Initialisiere welt entsprechend dim
    # a litte bit useless, but may be important for later stuff
    return np.zeros([dim,dim,dim])
# TRANSLATE WORLD
def move_z_down(world):
    # moves everything down
    newworld = world_init(30)
    for i in range(29):
        newworld[:,:,i] = world[:,:,i-1]

    return newworld

def move_z_up(world):
    # moves everything up
    newworld = world_init(30)
    for i in range(30):
        newworld[:,:,i] = world[:,:,i+1]

    return newworld

def move(world, stay=False, axis = 1,direction = 1):
    newworld = world_init(10)
    for i in range(0,9):
        if axis == 1:
            if direction == 1  and i<9:
                newworld[i+direction,:,:] = world[i,:,:]
            if direction == -1 and i>0:
                newworld[i,:,:] = world[i-direction,:,:]
        if axis == 2:
            if direction == 1  and i<9:
                newworld[:,i+direction,:] = world[:,i,:]
            if direction == -1 and i>0:
                newworld[:,i,:] = world[:,i-direction,:]
        if axis == 3:
            if direction == 1  and i<9:
                newworld[:,:,i+direction] = world[:,:,i]
            if direction == -1 and i>0:
                newworld[:,:,i] = world[:,:,i-direction]
    if stay:
        if axis == 1:
            if direction == 1  and i<9:
                newworld[9,:,:] = world[8,:,:] + world[9,:,:]
            if direction == -1 and i>0:
                newworld[0,:,:] = world[1,:,:] + world[0,:,:]
        if axis == 2:
            if direction == 1  and i<9:
                newworld[:,9,:] = world[:,8,:] + world[:,9,:]
            if direction == -1 and i>0:
                newworld[:,0,:] = world[:,0,:] + world[:,1,:]
        if axis == 3:
            if direction == 1  and i<9:
                newworld[:,:,9] = world[:,:,9] + world[:,:,8]
            if direction == -1 and i>0:
                newworld[:,:,0] = world[:,:,0] + world[:,:,1]

    return newworld


def move_y_down(world):
    # moves everything up
    newworld = world_init(30)
    for i in range(29):
        newworld[:,i,:] = world[:,i-1,:]

    return newworld

def move_y_up(world):
    # moves everything up
    newworld = world_init(30)
    for i in range(30):
        newworld[:,i,:] = world[:,i+1,:]

    return newworld

def move_x_down(world):
    # moves everything up
    newworld = world_init(30)
    for i in range(29):
        newworld[i,:,:] = world[i-1,:,:]

    return newworld

def move_x_up(world):
    # moves everything up
    newworld = world_init(30)
    for i in range(30):
        newworld[i,:,:] = world[i+1,:,:]

    return newworld



def rotate_x_90(world):
    #rotate world by 90 along x axis
    numpy.rot90(world,1,axes=(1,0,0))
    return world

def rotate_y_90(world,angle):
    #rotate world by 90 along y axis
    numpy.rot90(world,1,axes=(0,1,0))
    return world

def rotate_z_90(world,angle):
    #rotate world by 90 along z axis
    numpy.rot90(world,1,axes=(0,0,1))
    return world


def scale_x(world,a):
    # scale world along x axis by a pixel
    for x in range(10,20):
        for y in range(10,20):
            for z in range(10,20):
                if world [x+a,y,z]>0:
                    for i in range (0,a):
                        world[x+i,y,z]=world [x+(a-i),y,z]

    return world


def scale_y(world,a):
    # scale world along y axis by a pixel
    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                if world [x+a,y,z]>0:
                    for i in range (0,a):
                        world[x,y+i,z]=world [x,y,z]

    return world


def scale_z(world,a):
    # scale world along z axis by a pixel
    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                if world [x,y,z]>0:
                    for i in range (0,a):
                        world[x,y,z+i]=world [x,y,z]

    return world

def transform(x,y,z):
    '''
    Takes the world matrix (10*10*10) and
    converts the index to the coordinate matrix (100*3)
    '''
    return x + y * 10 + z * 100

def transform_2(world):
    '''
    Takes a world matrix and converts it into a textstring for the led cube
    '''
    newlist = np.zeros([len(world.flatten()),2])
    index = 0

    # Converting
    for x in range(10):
        for y in range(10):
            for z in range(10):
                if(y%2==0):
                    if x%2==0:
                        newlist[index,0] = ((x*10)+z+(y*100));
                    else:
                        newlist[index,0] = ((x*10)+9-z+(y*100));
                else:

                    if x%2==0:
                        newlist[index,0] = ((90-(x*10))+9-z+(y*100));
                    else:
                        newlist[index,0] = ((90-(x*10))+z+(y*100));
                newlist[index,1] = world[x,y,z]*255
                index += 1
    # Sort list
    sorted_newlist =  np.array(sorted(newlist,key=lambda x: x[0]))


    # Create textfile
    textfile = ''
    for i in sorted_newlist[:,1]:
        textfile = str(int(i))+','+textfile

    return textfile

def transform_3(world):
    '''
    Takes a world matrix and converts for direct streaming to the cube
    '''
    newlist = np.zeros([len(world.flatten()),2])
    index = 0

    # Converting
    for x in range(10):
        for y in range(10):
            for z in range(10):
                if(y%2==0):
                    if x%2==0:
                        newlist[index,0] = ((x*10)+z+(y*100));
                    else:
                        newlist[index,0] = ((x*10)+9-z+(y*100));
                else:

                    if x%2==0:
                        newlist[index,0] = ((90-(x*10))+9-z+(y*100));
                    else:
                        newlist[index,0] = ((90-(x*10))+z+(y*100));
                newlist[index,1] = world[x,y,z]*255
                index += 1

    # Sort list
    sorted_newlist =  np.array(sorted(newlist,key=lambda x: x[0]))

    return sorted_newlist

def world30toWorld10(world):
    newworld = world_init(10)
    for x in range(10):
        for y in range(10):
            for z in range(10):
                newworld[x,y,z] = world[x+10,y+10,z+10]

    return newworld

def gen_world_from_file(filename):
    # generates a world matrix from a file
    temp = np.genfromtxt(filename,delimiter=',')
    data = temp[:-1]
    world = world_init(10)
    for i in range(0,len(data)):
        position = (get_position(i))
        if data[i] > 0 :
            world[position[0],position[1],position[2]] = 1
    return world

def get_position(i):
    # calculates xyz from position in .vox string
    if i >= 100:  position = str(i)
    elif i >= 10: position = '0'+str(i)
    else :        position = '00'+str(i)

    # z coordinate, change every time
    if int(position[-2])%2 == 0:
        z = int(position[-1])
    else:
        z = 9 - int(position[-1])

    # y coordinate, changes every 10 times
    if int(position[-3])%2 == 0:
        y = int(position[-2])
    else:
        y = 9 - int(position[-2])

    # y coordinate, changes every 10 times
    x = int(position[-3])
    return x,y,z

# ------------------------------------------

def spawn_torus(world,r,R,xpos,ypos,zpos):
    #creates a torus
    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                if (((x+xpos)**2)+((y+ypos)**2)+((z+zpos)**2)+(R**2)-(r**2)) == 4*(R**2)*((x**2)+(y**2)):
                    world[x,y,z] = 1

    return world

def spawn_cone(world,a,phi,xpos,ypos,zpos):
    #creates a cone
    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                if (((x+xpos)**2+(y+ypos)**2)*(np.cos(phi)**2)) <= 0 and z >= 0+zpos and z <= a+zpos:
                    world[x,y,z] = 1

    return world


def spawn_plane(world,a,b,c,xpos,ypos,zpos):
    #creates a plane
    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                if (a*x+b*y+c*z) == -(a*xpos+b*ypos+c*zpos):
                    world[x,y,z] = 1

    return world


def spawn_cube(world,xpos,ypos,zpos,a,b,c):
    #creates a cube, plane, line, point
    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                if ((xpos-(a/2)) <= x <= (xpos+(a/2))) and ((ypos-(b/2)) <= y <= (ypos+(b/2))) and ((zpos-(c/2)) <= z <= (zpos+(c/2))):
                    world[x,y,z] = 1
    return world

def world_random(world):
    # Befuellt eine Welt mit zufaellig platzierten Einsen
    seed()
    for i in np.nditer(world, op_flags=['readwrite']):
        i += randint(0,1)

def spawn_sphere(world,radius,xpos,ypos,zpos):
    # creates a sphere with given parameters
    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                dist = np.sqrt((x-xpos)**2+(y-ypos)**2+(z-zpos)**2)
                if dist <= radius:
                    world[x,y,z] = 1

    return gaussian_filter(world,sigma=0.5)

def spawn_hollow_sphere(world,radius_in,radius_out,xpos,ypos,zpos):
    # creates hollow sphere with given parameters
    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                dist = np.sqrt((x-xpos)**2+(y-ypos)**2+(z-zpos)**2)
                if dist <= radius_out and dist >= radius_in:
                    world[x,y,z] = 1

    return world

def spawn_fading_line(world):
    x = randint(0,9)
    y = randint(0,9)

    if y % 2 :
        world[x,y,0] = 1.0
        world[x,y,1] = 0.9
        world[x,y,2] = 0.8
        world[x,y,3] = 0.7
        world[x,y,4] = 0.6
        world[x,y,5] = 0.5
        world[x,y,6] = 0.4
        world[x,y,7] = 0.3
        world[x,y,8] = 0.2
        world[x,y,9] = 0.1
    else:
        world[x,y,0] = 0.1
        world[x,y,1] = 0.2
        world[x,y,2] = 0.3
        world[x,y,3] = 0.4
        world[x,y,4] = 0.5
        world[x,y,5] = 0.6
        world[x,y,6] = 0.7
        world[x,y,7] = 0.8
        world[x,y,8] = 0.9
        world[x,y,9] = 1.0

    return world

# ------------------------------------------
# 3. Conway stuff

def number_of_neighbours(x,y,z,world):
    # super annoying routine to calculate number of neighbours
    # this is hard, since that damn cube isn't infinite,
    # but has edges and stuff

    # This is simple, neighbours away from borders
    if x > 0 and x < 9 and y > 0 and y < 9 and z > 0 and z < 9:
        non_diag_neighbours = world[x-1:x+2,y-1:y+2,z-1:z+2].cumsum()[-1] - world[x,y,z]

    # Dealing with x = 0 and x = 9
    elif x == 0 and y > 0 and y < 9 and z > 0 and z < 9:
        non_diag_neighbours = world[x:x+2,y-1:y+2,z-1:z+2].cumsum()[-1] - world[x,y,z] + world[-1,y-1:y+2,z-1:z+2].cumsum()[-1]

    elif x == 9 and y > 0 and y < 9 and z > 0 and z < 9:
        non_diag_neighbours = world[x-2:,y-1:y+2,z-1:z+2].cumsum()[-1] - world[x,y,z] + world[1,y-1:y+2,z-1:z+2].cumsum()[-1]

    # Dealing with y = 0 and y = 9
    elif x > 0 and x < 9 and y == 0 and z > 0 and z < 9:
        non_diag_neighbours = world[x-1:x+2,y:y+2,z-1:z+2].cumsum()[-1] - world[x,y,z] + world[x-1:x+2,-1,z-1:z+2].cumsum()[-1]

    elif x > 0 and x < 9 and y == 9 and z > 0 and z < 9:
        non_diag_neighbours = world[x-1:x+2,y-2:,z-1:z+2].cumsum()[-1] - world[x,y,z] + world[x-1:x+2,1,z-1:z+2].cumsum()[-1]

    # Dealing with z = 0 and z = 9
    elif z == 0 and x > 0 and x < 9 and y > 0 and y < 9:
        non_diag_neighbours = world[x-1:x+2,y-1:y+2,z:z+2].cumsum()[-1] - world[x,y,z] + world[x-1:x+2,y-1:y+2,-1].cumsum()[-1]

    elif z == 9 and x > 0 and x < 9 and y > 0 and y < 9:
        non_diag_neighbours = world[x-1:x+2,y-1:y+2,z-2:].cumsum()[-1] - world[x,y,z] + world[x-1:x+2,y-1:y+2,1].cumsum()[-1]

    # Dealing with edges

    # Edges of x and y
    elif x == 0 and y == 0 and z > 0 and z < 9:
        non_diag_neighbours = world[x:x+1,y:y+1,z-1:z+1].cumsum()[-1] - world[x,y,z] + world[-1,-1,z-1:z+1].cumsum()[-1]

    elif x == 0 and y == 9 and z > 0 and z < 9:
        non_diag_neighbours = world[x:x+1,y-2:,z-1:z+1].cumsum()[-1] - world[x,y,z] + world[-1,1,z-1:z+1].cumsum()[-1]

    elif x == 9 and y == 0 and z > 0 and z < 9:
        non_diag_neighbours = world[x-2:,y:y+1:,z-1:z+1].cumsum()[-1] - world[x,y,z] + world[1,-1,z-1:z+1].cumsum()[-1]

    elif x == 9 and y == 9 and z > 0 and z < 9:
        non_diag_neighbours = world[x-2:,y-2:,z-1:z+1].cumsum()[-1] - world[x,y,z] + world[1,1,z-1:z+1].cumsum()[-1]

    # Edges of x and z
    elif x == 0 and z == 0 and y > 0 and y < 9:
        non_diag_neighbours = world[x:x+1,y-1:y+1,z:z+1].cumsum()[-1] - world[x,y,z] + world[-1,y-1:y+1,-1].cumsum()[-1]

    elif x == 0 and z == 9 and y > 0 and y < 9:
        non_diag_neighbours = world[x:x+1,y-1:y+1,z-2:].cumsum()[-1] - world[x,y,z] + world[-1,y-1:y+1,1].cumsum()[-1]

    elif x == 9 and z == 0 and y > 0 and y < 9:
        non_diag_neighbours = world[x-2:,y-1:y+1:,z:z+1].cumsum()[-1] - world[x,y,z] + world[1,y-1:y+1,-1].cumsum()[-1]

    elif x == 9 and z == 9 and y > 0 and y < 9:
        non_diag_neighbours = world[x-2:,y-1:y+1,z-2:].cumsum()[-1] - world[x,y,z] + world[1,y-1:y+1,1].cumsum()[-1]

    # Edges of y and z
    elif x == 0 and z == 0 and y > 0 and y < 9:
        non_diag_neighbours = world[x-1:x+1,y:y+1,z:z+1].cumsum()[-1] - world[x,y,z] + world[x-1:x+1,-1,-1].cumsum()[-1]

    elif x == 0 and z == 9 and y > 0 and y < 9:
        non_diag_neighbours = world[x-1:x+1,y:y+1,z-2:].cumsum()[-1] - world[x,y,z] + world[x-1:x+1,-1,1].cumsum()[-1]

    elif x == 9 and z == 0 and y > 0 and y < 9:
        non_diag_neighbours = world[x-1:y+1,y-2:,z:z+1].cumsum()[-1] - world[x,y,z] + world[x-1:x+1,1,-1].cumsum()[-1]

    elif x == 9 and z == 9 and y > 0 and y < 9:
        non_diag_neighbours = world[x-1:y+1,y-2:,z-2:].cumsum()[-1] - world[x,y,z] + world[x-1:x+1,1,1].cumsum()[-1]

    else:
        non_diag_neighbours = 0
    return non_diag_neighbours


def evolve(world):
    # conway routine for one evolution step
    # change conway parameters here

    new_world = np.zeros([len(world),len(world),len(world)])
    for x in range(len(world)):
            for y in range(len(world)):
                for z in range(len(world)):
                    n_neighbours = number_of_neighbours(x,y,z,world)
                    #print x, y, z, n_neighbours
                    if n_neighbours < 8:
                        new_world[x,y,z] = 0
                    elif n_neighbours >= 18:
                        new_world[x,y,z] = 0
                    elif n_neighbours == 14:
                        new_world[x,y,z] = 1
                    else:
                        new_world[x,y,z] = world[x,y,z]

    return new_world

# ------------------------------------------
# 4. visualization

def visualize(world,nfig):
    # Shows world as a scatter plot

    # define coordinates (has to be fixed, is rotated against reality)
    coord = np.zeros([1000,3])
    coord[:,2] = [0]*100 + [1]*100 + [2]*100 + [3]*100 + [4]*100 + [5]*100 + [6]*100 + [7]*100 + [8]*100 + [9]*100
    coord[:,1] = ([0]*10 + [1]*10 + [2]*10 + [3]*10 + [4]*10 + [5]*10 + [6]*10 + [7]*10 + [8]*10 + [9]*10)*10
    coord[:,0] = [0,1,2,3,4,5,6,7,8,9]*100

    # define figure enviroment
    output = plt.figure(nfig)
    output.clf()
    fig = output.gca(projection='3d')
    fig.set_xlim(-1, 10)
    fig.set_ylim(-1, 10)
    fig.set_zlim(10, -1)

    fig.set_xlabel('X')
    fig.set_ylabel('Y')
    fig.set_zlabel('Z')

    fig = output.gca(projection='3d')

    # look where nonzero values are
    index_alive = np.asarray(np.where(world > 0)).T

    # create empty array for activated LEDs
    alive = np.zeros([0,3])

    for i in index_alive:
        # transform coordinates
        x = coord[transform(i[0],i[1],i[2]),0]
        y = coord[transform(i[0],i[1],i[2]),1]
        z = coord[transform(i[0],i[1],i[2]),2]
        # append activated led with correct coordinates
        alive = np.append(alive,[[x,y,z]], axis = 0)

    # parameters of viewing direction
    fig.view_init(elev=40, azim=50)
    fig.dist=12

    # plot
    fig.scatter(alive[:,0],alive[:,1],alive[:,2],color='red',marker='o',s=20)
    output.show()
