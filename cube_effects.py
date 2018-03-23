# modules
import numpy as np
from cube_utils import *
from scipy.signal import fftconvolve, gaussian

# Effects
# speed_decorator, blurs


def speed_decorator(function, frame, speed):
    '''
    Effect: Speed

    Use this to decorate other functions to gain speed control.
    Example:
    for i in range(20):
        world *= 0.5
        blub = speed_decorator(random, 3, i)
        world = blub(world, 3)
        print(i, world)
    '''
    # converting input
    speed = int((speed/127.0)*40+1)

    def simple_return(world, *args):
        return world

    if frame % speed is 0:
        return function
    else:
        return simple_return

def move(world, frame, achse, direction):

    achse = int(round((achse/127.0)*2))
    direction = int(round((direction/127.0)))

    if direction == 0: direction = -1

    newworld = np.roll(world, direction, axis=achse)

    return newworld



def blur(world, frame, x=1, y=1, z=1, amount=1, fade=0.9):
    '''
    Effect: Blur

    x   x blur on/off
    y   y blur on/off
    z   z blur on/off

    blurs the cube by spreading the values of each led
    onto the others
    '''
    # converting input
    x = int(round(x/127.0))
    y = int(round(y/127.0))
    z = int(round(z/127.0))
    amount = amount/127.0
    fade = fade/127.0

    # save previous max value for scaling
    old_max = world.max()

    # create gaussian window
    a = gaussian(5, amount+0.001, sym=True)

    dim = 7
    gauss = world_init(dim)
    center = dim/2

    '''
    if x != 1 or y != 1 or z != 1:
        if x == 1:
            gauss[center-2:center+3, center, center] = a[0]
            gauss[center-1:center+2, center, center] = a[1]
        if y == 1:
            gauss[center, center-2:center+3, center] = a[0]
            gauss[center, center-1:center+2, center] = a[1]
        if z == 1:
            gauss[center, center, center-2:center+3] = a[0]
            gauss[center, center, center-1:center+2] = a[1]
    else:
    '''

    gauss[center-2:center+3, center-2:center+3, center-2:center+3] = a[0]
    gauss[center-1:center+2, center-1:center+2, center-1:center+2] = a[1]

    gauss[center, center, center] = a[2]

    # convolute with gaussian
    world = fftconvolve(world, gauss, mode='same')

    # scale to 1
    #world /= world.max()+0.001

    # scale to old_max
    #world *= old_max

    return np.round(np.clip(world*fade, 0, 1), 2)

def color_translate(value):
    #translates values from 0 to 127 to rgb values
    if (value>126):
        value=126

    r_out = 0.0
    g_out = 0.0
    b_out = 0.0

    if(value<=21):
        r_out=1
        g_out=value/21.0
        b_out=0
    elif(value>21 and value<=42):
        r_out=1-((value-21.0)/21.0)
        g_out=1
        b_out=0
    elif(value>42 and value<=63):
        r_out=0
        g_out=1
        b_out=(value-42.0)/21.0
    elif(value>63 and value<=84):
        r_out=0
        g_out=1-((value-63.0)/21.0)
        b_out=1
    elif(value>84 and value<=105):
        r_out=(value-84.0)/21.0
        g_out=0
        b_out=1
    elif(value>105):
        r_out=1
        g_out=0
        b_out=1-((value-105.0)/21.0)

    return {'r':r_out, 'g':g_out, 'b':b_out}


def gradient(world, rgb1, rgb2, balance):
    if(balance<=0):
        balance=50.0
    else:
        balance = balance/127.0

    pixels_on = 1
    pixel_count = 0
    new_world_r = world_init(10)
    new_world_g = world_init(10)
    new_world_b = world_init(10)

    rgbResult1 = color_translate(rgb1)
    rgbResult2 = color_translate(rgb2)

    for x in range(len(world)):
        for y in range (len(world)):
            for z in range (len(world)):
                if(world[x,y,z]!=0):
                   pixels_on+=1


        for x in range(len(world)):
            for y in range (len(world)):
                for z in range (len(world)):
                    if(world[x,y,z]!=0):
                        if (pixel_count <= (pixels_on * balance)):
                            new_world_r[x,y,z]= world[x,y,z]*(rgbResult1['r']+(pixel_count/(pixels_on * balance))*rgbResult2['r'])
                            new_world_g[x,y,z]= world[x,y,z]*(rgbResult1['g']+(pixel_count/(pixels_on * balance))*rgbResult2['g'])
                            new_world_b[x,y,z]= world[x,y,z]*(rgbResult1['b']+(pixel_count/(pixels_on * balance))*rgbResult2['b'])
                            pixel_count+=1
                        elif (pixel_count > (pixels_on * balance)):
                            new_world_r[x,y,z]= world[x,y,z]*((1-((pixels_on * balance)/pixel_count))*rgbResult1['r']+rgbResult2['r'])
                            new_world_g[x,y,z]= world[x,y,z]*((1-((pixels_on * balance)/pixel_count))*rgbResult1['g']+rgbResult2['g'])
                            new_world_b[x,y,z]= world[x,y,z]*((1-((pixels_on * balance)/pixel_count))*rgbResult1['b']+rgbResult2['b'])
                            pixel_count+=1

        return {'r':new_world_r, 'g':new_world_g, 'b':new_world_b}


def gradient_sigmoidal(world, rgb1, rgb2, balance):

    if(balance<=0):
        balance=0.0001
    else:
        balance = balance/127.0

    pixels_on = 1
    pixel_count = 0
    new_world_r = world_init(10)
    new_world_g = world_init(10)
    new_world_b = world_init(10)

    rgbResult1 = color_translate(rgb1)
    rgbResult2 = color_translate(rgb2)

    for x in range(len(world)):
        for y in range (len(world)):
            for z in range (len(world)):
                if(world[x,y,z]!=0):
                   pixels_on+=1

    for x in range(len(world)):
            for y in range (len(world)):
                for z in range (len(world)):
                    if(world[x,y,z]!=0):
                        if (pixel_count <= (pixels_on * balance)):
                            new_world_r[x,y,z]= world[x,y,z]*((1-(1/(1+np.exp(1)**(5*((pixel_count/(balance * pixels_on))-1)))))*rgbResult1['r']+(1/(1+np.exp(1)**(5*((pixel_count/(balance * pixels_on))-1))))*rgbResult2['r'])
                            new_world_g[x,y,z]= world[x,y,z]*((1-(1/(1+np.exp(1)**(5*((pixel_count/(balance * pixels_on))-1)))))*rgbResult1['g']+(1/(1+np.exp(1)**(5*((pixel_count/(balance * pixels_on))-1))))*rgbResult2['g'])
                            new_world_b[x,y,z]= world[x,y,z]*((1-(1/(1+np.exp(1)**(5*((pixel_count/(balance * pixels_on))-1)))))*rgbResult1['b']+(1/(1+np.exp(1)**(5*((pixel_count/(balance * pixels_on))-1))))*rgbResult2['b'])
                            pixel_count+=1
                        elif (pixel_count > (pixels_on * balance)):
                            new_world_r[x,y,z]= world[x,y,z]*((1-(1/(1+np.exp(1)**(5*((pixel_count-(balance * pixels_on))/(pixels_on-(balance * pixels_on)))))))*rgbResult1['r']+(1/(1+np.exp(1)**(5*((pixel_count-(balance * pixels_on))/(pixels_on-(balance * pixels_on))))))*rgbResult2['r'])
                            new_world_g[x,y,z]= world[x,y,z]*((1-(1/(1+np.exp(1)**(5*((pixel_count-(balance * pixels_on))/(pixels_on-(balance * pixels_on)))))))*rgbResult1['g']+(1/(1+np.exp(1)**(5*((pixel_count-(balance * pixels_on))/(pixels_on-(balance * pixels_on))))))*rgbResult2['g'])
                            new_world_b[x,y,z]= world[x,y,z]*((1-(1/(1+np.exp(1)**(5*((pixel_count-(balance * pixels_on))/(pixels_on-(balance * pixels_on)))))))*rgbResult1['b']+(1/(1+np.exp(1)**(5*((pixel_count-(balance * pixels_on))/(pixels_on-(balance * pixels_on))))))*rgbResult2['b'])
                            pixel_count+=1
    return {'r':new_world_r, 'g':new_world_g, 'b':new_world_b}
