import numpy as np
#from random import randint, seed, random
#from scipy.special import jv

def world_init(dim):
    # Initialisiere welt entsprechend dim
    # a litte bit useless, but may be important for later stuff
    return np.zeros([dim, dim, dim])

'''
def world2coord(x, y, z):
    #Takes the world matrix (10*10*10) and
    #converts the index to the coordinate matrix (100*3)
    return x + y * 10 + z * 100
'''

'''
def world2vox(world):
    #Takes a world matrix and converts for direct streaming to the cube
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
'''

def world2vox(world):
    '''
    Takes a world matrix and converts for direct streaming to the cube
    '''
    newlist = np.zeros([len(world.flatten()),2],dtype=int)
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
                newlist[index,1] = int(world[x,y,z]*255)
                index += 1

    # Sort list
    sorted_newlist =  np.array(sorted(newlist,key=lambda x: x[0]))

    return sorted_newlist[:,1]

# unused

# ----------------------------------------------------
# for wave packet
'''
def propagate_step(world, dt=1.0):

    ntime = 20         # number of bessel functions

    def create_bessel(dt, ntime):
        # Returns numpy array with bessel functions
        c = []
        c.append(jv(0, dt))
        for m in range(1, ntime):
            c.append(2.0*(-1j)**m*jv(m, dt))

        return np.array(c)

    # create bessel functions
    bessel = create_bessel(dt, ntime)

    # create current wavefunction
    psi = world2list(world)

    # propagates wavefunction
    TmH = []
    TmH.append(psi)                 # 0
    TmH.append(np.dot(ham, psi))    # 1
    for n in range(2, ntime):       # 2 to ntime
        TmH.append(2.0 * np.dot(ham, TmH[-1]) - TmH[-2])

    # perform sum
    psiT = np.zeros(len(world)**3, dtype=np.complex)

    for m in range(ntime):
        psiT += bessel[m] * TmH[m]

    newworld = list2world(np.abs(psiT))

    return np.round(np.clip(newworld, 0, 1), 2)
'''

# ----------------------------------------------------

'''
def world2list(world):
    # Takes a world matrix and converts it to list

    newlist = np.zeros([len(world.flatten()), 2])
    index = 0

    # Converting
    for x in range(10):
        for y in range(10):
            for z in range(10):
                if(z % 2 == 0):
                    if y % 2 == 0:
                        newlist[index, 0] = (z*100) + (y*10) + x
                    else:
                        newlist[index, 0] = (z*100) + (y*10) + 9-x
                else:
                    if y % 2 == 0:
                        newlist[index, 0] = (z*100) + (90-y*10) + 9-x
                    else:
                        newlist[index, 0] = (z*100) + (90-y*10) + x
                newlist[index, 1] = world[x, y, z]
                index += 1

    # Sort list
    sorted_newlist = np.array(sorted(newlist, key=lambda x: x[0]))

    return sorted_newlist[:, 1]
'''

'''
def list2world(liste):
    # creates list from world file
    world = world_init(10)

    for i in range(0, len(liste)):
        position = (get_position(i))
        if liste[i] > 0:
            world[position[0], position[1], position[2]] = liste[i]
    return world
'''

'''
def get_position(i):
    # calculates xyz from position in list
    if i >= 100:
        position = str(i)
    elif i >= 10:
        position = '0'+str(i)
    else:
        position = '00'+str(i)

    if int(position[0]) % 2 == 0:
        if int(position[1]) % 2 == 0:
            x = int(position[2])
            y = int(position[1])
            z = int(position[0])
        else:
            x = 9-int(position[2])
            y = int(position[1])
            z = int(position[0])
    else:
        if int(position[1]) % 2 == 0:
            x = int(position[2])
            y = 9-int(position[1])
            z = int(position[0])
        else:
            x = 9-int(position[2])
            y = 9-int(position[1])
            z = int(position[0])

    return x, y, z
'''
