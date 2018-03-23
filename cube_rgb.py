# ------ modules ------
import numpy as np
from cube_utils import world_init


def createRGBWorld(world):
    world_r = world_init(10)
    world_g = world_init(10)
    world_b = world_init(10)

    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                world_r[x,y,z]=world[x,y,z]
                world_g[x,y,z]=world[x,y,z]
                world_b[x,y,z]=world[x,y,z]

    return {'r':world_r, 'g':world_g, 'b':world_b}

def combineRGBWorlds(world1r,world1g,world1b,world2r,world2g,world2b):
    world_r = world_init(10)
    world_g = world_init(10)
    world_b = world_init(10)

    for x in range(len(world_r)):
        for y in range(len(world_r)):
            for z in range(len(world_r)):
                world_r[x,y,z]=(world1r[x,y,z]+world2r[x,y,z])/2
                world_g[x,y,z]=(world1g[x,y,z]+world2g[x,y,z])/2
                world_b[x,y,z]=(world1b[x,y,z]+world2b[x,y,z])/2

    return {'r':world_r, 'g':world_g, 'b':world_b}

def manipulateRGBWorld(world_r,world_g,world_b, value_r, value_g, value_b):
    new_world_r = world_init(10)
    new_world_g = world_init(10)
    new_world_b = world_init(10)

    for x in range(len(world_r)):
        for y in range(len(world_r)):
            for z in range(len(world_r)):
                new_world_r[x,y,z]=world_r[x,y,z]*value_r
                new_world_g[x,y,z]=world_g[x,y,z]*value_g
                new_world_b[x,y,z]=world_b[x,y,z]*value_b

    return {'r':new_world_r, 'g':new_world_g, 'b':new_world_b}

def generateRainbowWorld(world, red, green, blue, speed):
    new_world_r = world_init(10)
    new_world_g = world_init(10)
    new_world_b = world_init(10)

    if(red>0.99 and blue<0.99 and green<0.01):
        blue = blue+speed
    elif(blue>0.99 and red>0.01 and green<0.01):
        red = red-speed
    elif(blue>0.99 and green<0.99 and red<0.01):
        green = green+speed
    elif(green>0.99 and blue>0.01 and red<0.01):
        blue = blue-speed
    elif(green>0.99 and red<0.99 and blue<0.01):
        red = red+speed
    elif(red>0.99 and green>0.01 and blue<0.01):
        green = green-speed

    red, blue, green = np.clip([red,blue,green],0,1)

    for x in range(len(world)):
        for y in range(len(world)):
            for z in range(len(world)):
                if(world[x,y,z]!=0):
                    new_world_b[x,y,z]=blue
                    new_world_r[x,y,z]=red
                    new_world_g[x,y,z]=green

    return {'r':new_world_r, 'g':new_world_g, 'b':new_world_b, 'rW':red,'gW':green,'bW':blue,}
