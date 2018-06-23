# modules
import numpy as np


class e_rainbow():
    '''
    Effect: fade2self.blue

    fades the cube to self.blue by moving some of the self.green and self.red
    to the self.blue

    Parameters:
    - amount: how much is moved from the r/g channel to the b channel
    '''

    def __init__(self):

        self.c1 = {'r':1.0, 'g':0.0, 'b':0.0}
        self.c2 = {'r':0.0, 'g':0.0, 'b':1.0}
        self.balance = 0.5

    def control(self, c1, c2, balance):
        self.c1 = color_translate(c1)
        self.c2 = color_translate(c2)
        self.balance = balance

    def label(self):
        return ['c1',self.c1,'c2', self.c2,'balance',round(self.balance,2)]  

    def generate(self, step, world):



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

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    if(world[:, x,y,z]!=0):
                        pixels_on+=1

        for x in range(10):
            for y in range(10):
                for z in range(10):
                    if(world[:, x,y,z]!=0):
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


        world[0,:,:,:] = new_world_r
        world[1,:,:,:] = new_world_g
        world[2,:,:,:] = new_world_b

        return np.clip(world, 0, 1)


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


def color_translate(value):
    value *= 127
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
