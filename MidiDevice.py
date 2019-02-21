
import time as time
from rtmidi.midiutil import open_midiinput,open_midioutput
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF,CONTROL_CHANGE
from global_parameter_module import global_parameter
#Globals
MidiKeyIn = 0
MidiValueIn = 0
MidiChannelIn = 0
input_dict = {}

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        # output = message
        #print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        #print(message[1],message[2])
        global MidiChannelIn
        MidiChannelIn = message[0]
        global MidiKeyIn
        MidiKeyIn = message[1]
        global MidiValueIn
        MidiValueIn = message[2]
        global input_dict
        input_dict.update({MidiKeyIn:MidiValueIn})
        global_parameter[message[1]] = message[2]

class GlobalParameterHandler:
    def __init__(self):
        self.globalCommandArray = np.zeros(255)
        self.MidiKeyGloabalKeyDict = {
        0:0,#Knob1 :
        1:1,
        2:2,
        3:3,
        4:4,
        5:5,
        6:6,
        7:7,
        8:8,
        9:9,
        10:10,
        11:11,
        12:12,
        13:13,
        14:14,
        15:15
        }


    def setParameters(self,channel,key,value):
        if(channel==1):


class MidiDevice:
    def __init__(self,in_port,out_port):
        print("Initialize MIDI CONTROL")
        global input_dict
        self.input_port = in_port
        self.midiin, self.portname_in = open_midiinput(self.input_port)
        self.Handler = MidiInputHandler(self.portname_in)
        self.midiin.set_callback(self.Handler)

        self.output_port = out_port
        self.midiout, self.portname_out = open_midioutput(self.output_port)

        self.color = 0x01

        self.cc0 = CONTROL_CHANGE | 0x00
        self.cc1 = CONTROL_CHANGE | 0x01
        self.cc2 = CONTROL_CHANGE | 0x02
        self.cc3 = CONTROL_CHANGE | 0x03
        self.cc4 = CONTROL_CHANGE | 0x04
        self.cc5 = CONTROL_CHANGE | 0x05
        self.cc6 = CONTROL_CHANGE | 0x06
        self.cc8 = CONTROL_CHANGE | 0x08
        self.makeRingBlink(0x00)
        self.makeRingBlink(0x04)
        self.makeRingBlink(0x08)
        self.makeRingBlink(0x0B)
        self.makeRainbow(0x01)
        self.makeLedBlink(0x05)
        self.stopBlink(0x0B)
        #time.sleep(1)
        #self.midiout.send_message([0xB2,0x00,0x3C])
        #time.sleep(1)
        #self.midiout.send_message([0xB3,0x00,0x04])


    def logMidi(self):
        print("Midi Channel :"+str(MidiChannelIn)+" | Midi Key :"+str(MidiKeyIn)+" | Midi Value : "+str(MidiValueIn))
        self.setRGB(0x03,self.color)
        self.color+=0x01
        root.after(500, test.logMidi)

    def read(self):
        return input_dict

    def send(self,Key,Value):
        self.midiout.send_message([self.cc0,Key,Value])

    def makeRingBlink(self,Key):
        self.midiout.send_message([0xB2,Key,0x3C])
        self.midiout.send_message([0xB3,Key,0x04])
    def makeRainbow(self,Key):
        self.midiout.send_message([0xB2,Key,0x7F])
    def makeLedBlink(self,Key):
        self.midiout.send_message([0xB2,Key,0x0C])
    def stopBlink(self,Key):
        self.midiout.send_message([0xB2,Key,0x00])
    def setRGB(self,Key,Color):
        self.midiout.send_message([0xB1,Key,Color])
