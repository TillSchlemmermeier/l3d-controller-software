from Tkinter import *
from cube_utils import *
#from cube_animations import rain_gen, gen_dots, plain_gen
#from cube_interactive import dots_on_sphere, random, sphere, speed_decorator, hsphere, planes, lines, cube, corner, circle, blur, moveandfade, seperate, blow, random_lines
from cube_rgb import createRGBWorld,combineRGBWorlds,manipulateRGBWorld, generateRainbowWorld
from cube_effects import *
from cube_generators import *
from math import *
import serial
import sys,os,glob,time
import numpy as np
import struct
import inspect
from rtmidi.midiutil import open_midiinput
from copy import deepcopy

MidiKey = 0
MidiValue = 0

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        frame=Frame(self)
        frame.pack()

        #CONECTION
        try:
            self.con = serial.Serial('/dev/ttyACM0',230400)
            print self.con
        except IOError:
            self.con = serial.Serial('/dev/ttyACM1',230400)
            print self.con

        #VARS
        self.do_send = False
        self.transworld = world_init(10)
        self.do_send_rgb = False

        self.transworld_R = world_init(10)
        self.transworld_G = world_init(10)
        self.transworld_B = world_init(10)

        self.transworld_R_old = world_init(10)
        self.transworld_G_old = world_init(10)
        self.transworld_B_old = world_init(10)
        self.cubedata = world2vox(self.transworld)

        self.cubedata_R = world2vox(self.transworld_R)
        self.cubedata_G = world2vox(self.transworld_G)
        self.cubedata_B = world2vox(self.transworld_B)
        self.cubecolor1_r = 1.0;
        self.cubecolor1_g = 1.0;
        self.cubecolor1_b = 1.0;
        self.cubecolor2_r = 1.0;
        self.cubecolor2_g = 1.0;
        self.cubecolor2_b = 1.0;

        self.framecount = 0
        self.send_array = bytearray(1009)
        self.send_array_rgb = bytearray(3009)
        self.FadeValue = 0.5
        self.DimValue= 1.0
        #Generators and Effects
        self.generators = ["NONE","random_gen","random_sphere_gen", "lines_gen", "cube_gen", "corner_static_gen", "randomlines_gen","block_gen", "growing_sphere_gen", "dots_on_sphere_gen", "osci_planes_gen", "randomlinesY_gen","corner_random_gen", "passing_planes_gen","random_block_gen", "random_block_outlines_gen"]
        self.effects = ["NONE","blur_eff", "move_eff","gradient_eff"]
        #Midi Controller Assignment
        self.arg1G1 = 0
        self.arg2G1 = 0
        self.arg3G1 = 0
        self.arg4G1 = 0
        self.arg5G1 = 0
        self.arg6G1 = 0

        self.arg1G2 = 0
        self.arg2G2 = 0
        self.arg3G2 = 0
        self.arg4G2 = 0
        self.arg5G2 = 0
        self.arg6G2 = 0

        self.arg1E1 = 0
        self.arg2E1 = 0
        self.arg3E1 = 0
        self.arg4E1 = 0
        self.arg5E1 = 0
        self.arg6E1 = 0

        self.arg1E2 = 0
        self.arg2E2 = 0
        self.arg3E2 = 0
        self.arg4E2 = 0
        self.arg5E2 = 0
        self.arg6E2 = 0
        #Header Information
        self.hSpeed = 1
        self.hBright = 200
        self.hPal=1
        self.hPalMode=0
        self.hRGBMOde=0
        #sendspeed
        self.sendSpeed=35
        #Rainbow Vars
        self.rainbow_r1=1.0
        self.rainbow_g1=0
        self.rainbow_b1=0
        self.rainbowSpeed1=0.05
        self.rainbow_r2=0
        self.rainbow_g2=1.0
        self.rainbow_b2=0
        self.rainbowSpeed2=0.05

        #GUI Elements
        self.startButton = Button(frame,text="Start",command=self.startsending)
        self.startButton.grid(row = 0, column =4 )

        self.stopButton = Button(frame,text="Stop",command=self.stopsending)
        self.stopButton.grid(row = 0, column = 5 )

        self.labelG1 = Label(frame, text="Generator 1")
        self.labelG1.grid(row = 1, column = 0)

        self.labelG2 = Label(frame, text="Generator 2")
        self.labelG2.grid(row = 1, column = 1)

        self.labelE1 = Label(frame, text="Effekt 1")
        self.labelE1.grid(row = 1, column = 2)

        self.labelE2 = Label(frame, text="Effekt 2")
        self.labelE2.grid(row = 1, column = 3)

        self.dropdownG1Current = StringVar()
        self.dropdownG1Current.set(self.generators[0])
        self.dropdownG1 = OptionMenu(frame,self.dropdownG1Current,*self.generators)
        self.dropdownG1.grid(row = 2, column = 0)

        self.dropdownG2Current = StringVar()
        self.dropdownG2Current.set(self.generators[0])
        self.dropdownG2 = OptionMenu(frame,self.dropdownG2Current,*self.generators)
        self.dropdownG2.grid(row = 2, column = 1)

        self.dropdownE1Current = StringVar()
        self.dropdownE1Current.set(self.effects[0])
        self.dropdownE1 = OptionMenu(frame,self.dropdownE1Current,*self.effects)
        self.dropdownE1.grid(row = 2, column = 2)

        self.dropdownE2Current = StringVar()
        self.dropdownE2Current.set(self.effects[0])
        self.dropdownE2 = OptionMenu(frame,self.dropdownE2Current,*self.effects)
        self.dropdownE2.grid(row = 2, column = 3)

#L3D-Functions
    def startsending(self):
        self.do_send_rgb=True
        self.send_data_rgb()

    def stopsending(self):
        self.do_send_rgb=False

    # Generators
    def growing_sphere_gen(self, speed2, wait, bonl1, bonk2, bonk3, speed):
        blub = speed_decorator(growing_sphere, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, speed2, wait)

    def dots_on_sphere_gen(self, number, radius, bonk1, bonk2, bonk3, speed):
        blub = speed_decorator(dots_on_sphere, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, number, radius )

    def block_gen(self,number, sx, sy, sz, bonk, speed):
        blub = speed_decorator(block, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, sx, sy, sz)

    def dottedSphere(self, number, radius, bonk3, boin4, bonk5, speed):
        blub = speed_decorator(dots_on_sphere, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, number, radius)

    def random_gen(self, number, bonk1, bonk2, bonk3, bonk4, speed):
        blub = speed_decorator(random, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount,number)

    def random_sphere_gen(self, radius, bonk1, bonk2, bonk3, bonk4, speed):
        blub = speed_decorator(randomsphere, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount,radius)

#    def hsphere_gen(self,radius, xpos, ypos, zpos, bonk1, speed):
#        blub = speed_decorator(hsphere, self.framecount, speed)
#        self.transworld = blub(self.transworld, self.framecount,radius,xpos,ypos,zpos)

    def planes_gen(self,vx, vy, vz, j, bonk1, speed):
        blub = speed_decorator(planes, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount,vx,vy,vz,j)

    def lines_gen(self,bonk1,bonk2, bonk3, bonk4, bonk5, speed):
        blub = speed_decorator(lines, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount)

    def randomlines_gen(self,bonk1,bonk2, bonk3, bonk4, bonk5, speed):
        blub = speed_decorator(random_lines, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount)

    def randomlinesY_gen(self,bonk1,bonk2, bonk3, bonk4, bonk5, speed):
        blub = speed_decorator(random_lines_Y, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount,bonk1,bonk2)

    def circle_gen(self, height,bonk2, bonk3, bonk4, bonk5, speed):
        blub = speed_decorator(moving_circle, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount,height)

    def corner_static_gen(self, size,bonk2, bonk3, bonk4, bonk5, speed):
        blub = speed_decorator(corner_static, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, size)

    def corner_random_gen(self, number,size, bonk3, bonk4, bonk5, speed):
        blub = speed_decorator(corner_random    , self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, number, size)

    def cube_gen(self, size,bonk2, bonk3, bonk4, bonk5, speed):
        blub = speed_decorator(cube, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, size)

    def osci_planes_gen(self, movespeed, size, direction, bonk4, bonk5, speed):
        blub = speed_decorator(osci_planes, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, movespeed, size, direction)

    def passing_planes_gen(self, movespeed, size, direction, bonk4, bonk5, speed):
        blub = speed_decorator(passing_planes, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, movespeed, size, direction)
    def random_block_gen(self, sizeX, sizeY, sizeZ, bonk4, bonk5, speed):
        blub = speed_decorator(random_block, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, sizeX, sizeY, sizeZ)
    def random_block_outlines_gen(self,sizeX, sizeY, sizeZ, bonk4, bonk5, speed):
        blub = speed_decorator(random_block_outlines, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, sizeX, sizeY, sizeZ)

    # effects

    def blur_eff(self, bonk1, bonk2, bonk3, bonk4, bonk5, speed):
        # blur(world, frame, x=1, y=1, z=1, amount=1, fade=0.9)
        blub = speed_decorator(blur, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount,bonk1, bonk2, bonk3, bonk4, bonk5)

    #def blow_eff(self, bonk1, bonk2, bonk3, bonk4, bonk5, speed):
    #    # blur(world, frame, x=1, y=1, z=1, amount=1, fade=0.9)
    #    blub = speed_decorator(blow, self.framecount, speed)
    #    self.transworld = blub(self.transworld, self.framecount)

    #def seperate_eff(self, direction, bonk2, bonk3, bonk4, bonk5, speed):
    #    # blur(world, frame, x=1, y=1, z=1, amount=1, fade=0.9)
    #    blub = speed_decorator(seperate, self.framecount, speed)
    #    self.transworld = blub(self.transworld, self.framecount, direction)

    def move_eff(self, axis, direction, bonk1, bonk4, bonk5, speed):
        # moveandfade(world, frame, axis=1, direction=1, fade=1.0)
        blub = speed_decorator(move, self.framecount, speed)
        self.transworld = blub(self.transworld, self.framecount, axis, direction)

    def gradient_eff(self, rgb1, rgb2, balance, bonk1, bonk2, speed):
        #blub = speed_decorator(gradient, self.framecount, speed)
        #self.transworld = blub(self.transworld, rgb1, rgb2, balance)
        gradientResult = gradient_sigmoidal(self.transworld, rgb1, rgb2, balance)
        self.transworld_R = gradientResult['r']
        self.transworld_G = gradientResult['g']
        self.transworld_B = gradientResult['b']

    def apply_manipulation(self):
        #Generator 1
        self.transworld = world_init(10)

        self.transworld_R = world_init(10)
        self.transworld_G = world_init(10)
        self.transworld_B = world_init(10)

        if(MidiKey==16): self.arg1G1 = MidiValue
        if(MidiKey==17): self.arg2G1 = MidiValue
        if(MidiKey==18): self.arg3G1 = MidiValue
        if(MidiKey==20): self.arg4G1 = MidiValue
        if(MidiKey==21): self.arg5G1 = MidiValue
        if(MidiKey==22): self.arg6G1 = MidiValue

        if(self.dropdownG1Current.get()!="NONE"):
            self.fullFunctionG1 = "self."+self.dropdownG1Current.get()+"("+str(self.arg1G1)+","+str(self.arg2G1)+","+str(self.arg3G1)+","+str(self.arg4G1)+","+str(self.arg5G1)+","+str(self.arg6G1)+")"
            exec(self.fullFunctionG1)

        rgbresult1 = createRGBWorld(self.transworld)
        self.transworld_R = rgbresult1['r']
        self.transworld_G = rgbresult1['g']
        self.transworld_B = rgbresult1['b']

        if(self.dropdownE1Current.get()!="gradient_eff"):
            if MidiKey==19 :
                self.cubecolor1_r = MidiValue/128.0
            if MidiKey==23 :
                self.cubecolor1_g = MidiValue/128.0
            if MidiKey==27 :
                self.cubecolor1_b = MidiValue/128.0
            if MidiKey==57 :
                self.rainbowSpeed1 = MidiValue/1280.0
            if(self.cubecolor1_r<0.2 and self.cubecolor1_g<0.2 and self.cubecolor1_b<0.2 ):
                rgbresult1 = generateRainbowWorld(self.transworld,self.rainbow_r1,self.rainbow_g1,self.rainbow_b1, self.rainbowSpeed1)
                self.rainbow_r1 = rgbresult1['rW']
                self.rainbow_g1 = rgbresult1['gW']
                self.rainbow_b1 = rgbresult1['bW']
                # print(self.rainbow_r, self.rainbow_g, self.rainbow_b)
            else:
                rgbresult1 = manipulateRGBWorld(rgbresult1['r'],rgbresult1['g'],rgbresult1['b'],self.cubecolor1_r,self.cubecolor1_g,self.cubecolor1_b)
        else:
            rgbresult1={'r':self.transworld_R ,'g':self.transworld_G, 'b':self.transworld_B}


        if(MidiKey==46): self.arg1E1 = MidiValue
        if(MidiKey==47): self.arg2E1 = MidiValue
        if(MidiKey==48): self.arg3E1 = MidiValue
        if(MidiKey==50): self.arg4E1 = MidiValue
        if(MidiKey==51): self.arg5E1 = MidiValue
        if(MidiKey==52): self.arg6E1 = MidiValue

        if(self.dropdownE1Current.get()!="NONE"):
            self.fullFunctionE1 = "self."+self.dropdownE1Current.get()+"("+str(self.arg1E1)+","+str(self.arg2E1)+","+str(self.arg3E1)+","+str(self.arg4E1)+","+str(self.arg5E1)+","+str(self.arg6E1)+")"
            exec(self.fullFunctionE1)

        if(MidiKey==54): self.arg1E2 = MidiValue
        if(MidiKey==55): self.arg2E2 = MidiValue
        if(MidiKey==56): self.arg3E2 = MidiValue
        if(MidiKey==58): self.arg4E2 = MidiValue
        if(MidiKey==59): self.arg5E2 = MidiValue
        if(MidiKey==60): self.arg6E2 = MidiValue

        if(self.dropdownE2Current.get()!="NONE"):
            self.fullFunctionE2 = "self."+self.dropdownE2Current.get()+"("+str(self.arg1E2)+","+str(self.arg2E2)+","+str(self.arg3E2)+","+str(self.arg4E2)+","+str(self.arg5E2)+","+str(self.arg6E2)+")"
            exec(self.fullFunctionE2)

        #Generator 2
        self.transworld = world_init(10)

        if(MidiKey==24): self.arg1G2 = MidiValue
        if(MidiKey==25): self.arg2G2 = MidiValue
        if(MidiKey==26): self.arg3G2 = MidiValue
        if(MidiKey==28): self.arg4G2 = MidiValue
        if(MidiKey==29): self.arg5G2 = MidiValue
        if(MidiKey==30): self.arg6G2 = MidiValue

        if(self.dropdownG2Current.get()!="NONE"):
            self.fullFunctionG2 = "self."+self.dropdownG2Current.get()+"("+str(self.arg1G2)+","+str(self.arg2G2)+","+str(self.arg3G2)+","+str(self.arg4G2)+","+str(self.arg5G2)+","+str(self.arg6G2)+")"
            exec(self.fullFunctionG2)

        if(MidiKey==46): self.arg1E1 = MidiValue
        if(MidiKey==47): self.arg2E1 = MidiValue
        if(MidiKey==48): self.arg3E1 = MidiValue
        if(MidiKey==50): self.arg4E1 = MidiValue
        if(MidiKey==51): self.arg5E1 = MidiValue
        if(MidiKey==52): self.arg6E1 = MidiValue

        if(self.dropdownE1Current.get()!="NONE"):
            self.fullFunctionE1 = "self."+self.dropdownE1Current.get()+"("+str(self.arg1E1)+","+str(self.arg2E1)+","+str(self.arg3E1)+","+str(self.arg4E1)+","+str(self.arg5E1)+","+str(self.arg6E1)+")"
            exec(self.fullFunctionE1)

        if(MidiKey==54): self.arg1E2 = MidiValue
        if(MidiKey==55): self.arg2E2 = MidiValue
        if(MidiKey==56): self.arg3E2 = MidiValue
        if(MidiKey==58): self.arg4E2 = MidiValue
        if(MidiKey==59): self.arg5E2 = MidiValue
        if(MidiKey==60): self.arg6E2 = MidiValue

        if(self.dropdownE2Current.get()!="NONE"):
            self.fullFunctionE2 = "self."+self.dropdownE2Current.get()+"("+str(self.arg1E2)+","+str(self.arg2E2)+","+str(self.arg3E2)+","+str(self.arg4E2)+","+str(self.arg5E2)+","+str(self.arg6E2)+")"
            exec(self.fullFunctionE2)

        #self.cubedata = transform_3(self.transworld)
        if(self.dropdownE1Current.get()!="gradient_eff"):
            rgbresult2 = createRGBWorld(self.transworld)
            if MidiKey==31 :
                self.cubecolor2_r = MidiValue/128.0
            if MidiKey==49 :
                self.cubecolor2_g = MidiValue/128.0
            if MidiKey==53 :
                self.cubecolor2_b = MidiValue/128.0
            if MidiKey==61 :
                self.rainbowSpeed2 = MidiValue/1280.0
            if(self.cubecolor2_r<0.2 and self.cubecolor2_g<0.2 and self.cubecolor2_b<0.2 ):
                rgbresult2 = generateRainbowWorld(self.transworld,self.rainbow_r2,self.rainbow_g2,self.rainbow_b2, self.rainbowSpeed2)
                self.rainbow_r2 = rgbresult2['rW']
                self.rainbow_g2 = rgbresult2['gW']
                self.rainbow_b2 = rgbresult2['bW']
                # print(self.rainbow_r, self.rainbow_g, self.rainbow_b)
            else:
                rgbresult2 = manipulateRGBWorld(rgbresult2['r'],rgbresult2['g'],rgbresult2['b'],self.cubecolor2_r,self.cubecolor2_g,self.cubecolor2_b)
        else:
            rgbresult2 = {'r':self.transworld_R ,'g':self.transworld_G, 'b':self.transworld_B}

        rgbresult3 = combineRGBWorlds(rgbresult1['r'],rgbresult1['g'],rgbresult1['b'],rgbresult2['r'],rgbresult2['g'],rgbresult2['b'])

        rgbresult3['r'] += self.transworld_R_old*self.FadeValue
        rgbresult3['g'] += self.transworld_G_old*self.FadeValue
        rgbresult3['b'] += self.transworld_B_old*self.FadeValue

        rgbresult3['r'] *= self.DimValue
        rgbresult3['g'] *= self.DimValue
        rgbresult3['b'] *= self.DimValue

        self.cubedata_R = world2vox(np.clip(rgbresult3['r'],0,1))
        self.cubedata_G = world2vox(np.clip(rgbresult3['g'],0,1))
        self.cubedata_B = world2vox(np.clip(rgbresult3['b'],0,1))

        self.transworld_R_old = deepcopy(rgbresult3['r'])
        self.transworld_G_old = deepcopy(rgbresult3['g'])
        self.transworld_B_old = deepcopy(rgbresult3['b'])
        #if MidiKey==61 :
        #    self.sendSpeed=MidiValue
        if MidiKey==62 :
            self.FadeValue = np.clip(MidiValue/128.0,0,1)
        if MidiKey==60 :
            self.DimValue = np.clip(MidiValue/128.0,0,1)
        #if MidiKey==23 :
        #    self.hBright=MidiValue*2
        #if MidiKey==27 :
        #    self.hPal= int(MidiValue/(128.0/10))+1
        #if MidiKey==31 :
        #    self.hPalMode= int(MidiValue/(127.0/3))


    def send_data(self):
        if self.do_send:
            #Package that shit with a nice header
            self.send_array[0] = struct.pack('>B',66)#B
            self.send_array[1] = struct.pack('>B',69)#E
            self.send_array[2] = struct.pack('>B',69)#E
            self.send_array[3] = struct.pack('>B',70)#F
            self.send_array[4] = struct.pack('>B',self.hSpeed)#SPEED
            self.send_array[5] = struct.pack('>B',self.hBright)#'Bright'
            self.send_array[6] = struct.pack('>B',self.hPalMode)#PalMODE
            self.send_array[7] = struct.pack('>B',self.hPal)#PalSELECT
            self.send_array[8] = struct.pack('>B',0)#BW/RGB
            count = 9

            for i in self.cubedata[:,1]:
                if MidiKey == 27 and MidiValue == 127:
                    self.send_array[count] = struct.pack('>B',int(0))
                elif MidiKey == 26 and MidiValue == 127:
                    if self.framecount % 2:
                        self.send_array[count] = struct.pack('>B',int(0))
                    else:
                        self.send_array[count] = struct.pack('>B',int(i))
                else:
                    self.send_array[count] = struct.pack('>B',int(i))
                count=count+1

            self.framecount+=1
            #send the fuckin package
            self.con.write(self.send_array)
            self.apply_manipulation()
            self.after( 20, self.send_data)

    def send_data_rgb(self):
        if self.do_send_rgb:
            #compute animation
            self.apply_manipulation()
            #Package that shit with a nice header
            self.send_array_rgb[0] = struct.pack('>B',66)#B
            self.send_array_rgb[1] = struct.pack('>B',69)#E
            self.send_array_rgb[2] = struct.pack('>B',69)#E
            self.send_array_rgb[3] = struct.pack('>B',70)#F
            self.send_array_rgb[4] = struct.pack('>B',self.hSpeed)#SPEED
            self.send_array_rgb[5] = struct.pack('>B',self.hBright)#'Bright'
            self.send_array_rgb[6] = struct.pack('>B',self.hPalMode)#PalMODE
            self.send_array_rgb[7] = struct.pack('>B',self.hPal)#PalSELECT
            self.send_array_rgb[8] = struct.pack('>B',1)#BW/RGB
            count = 9

            for r,g,b in zip(self.cubedata_R[:,1],self.cubedata_G[:,1],self.cubedata_B[:,1]):
                #print(r,g,b)
                self.send_array_rgb[count] = struct.pack('>B',int(r))
                self.send_array_rgb[count+1] = struct.pack('>B',int(g))
                self.send_array_rgb[count+2] = struct.pack('>B',int(b))
                count=count+3

            self.framecount+=1
            #send the fuckin package
            self.con.write(self.send_array_rgb)
            self.after( self.sendSpeed, self.send_data_rgb)

# -----------------------------------------
# midi routines
class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        #output = message
        #print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        #print(message[1],message[2])
        global MidiKey
        MidiKey = message[1]
        global MidiValue
        MidiValue = message[2]

# -----------------------------------------

if __name__ == "__main__":

    # Initialize MIDI INPUT
    port = 1
    #try:
    midiin, port_name = open_midiinput(port)
    #except (EOFError, KeyboardInterrupt):
    #    sys.exit()

    print("Attaching MIDI input callback handler.")
    midiin.set_callback(MidiInputHandler(port_name))

    print("Starting main.")
    # midi ready

    root = App()
    root.title("PyControll")
    root.mainloop()
