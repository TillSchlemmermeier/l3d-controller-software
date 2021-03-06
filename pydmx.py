#!/usr/bin/env python

import msvcrt
import serial
import sys
import time


class pydmx(object):
        def __init__(self, port_number=2):
                self.channels = [0 for i in range(512)]
                self.port_number = port_number

                # DMX_USB Interface variables
                self.SOM_VALUE = 0x7E # SOM = Start of Message
                self.EOM_VALUE = 0xE7 # EOM = End of Message

                # Lables:
                self.REPROGRAM_FIRMWARE_LABEL           = 1
                self.PROGRAM_FLASH_PAGE_LABEL           = 2
                self.GET_WIDGET_PARAMETERS_LABEL        = 3
                self.SET_WIDGET_PARAMETERS_LABEL        = 4
                self.RECEIVED_DMX_LABEL	                = 5
                self.OUTPUT_ONLY_SEND_DMX_LABEL         = 6
                self.RDM_SEND_DMX_LABEL                 = 7
                self.RECIEVE_DMX_ON_CHANGE_LABEL        = 8
                self.RECIEVED_DMX_CHANGE_OF_STATE_LABEL = 9
                self.GET_WIDGET_SERIAL_NUMBER_LABEL     = 10
                self.SEND_RDM_DISCOVERY_LABEL           = 11
                self.INVALID_LABEL                      = 0xFF

                # Initialize serial port
                try:
                	# Open serial port with receive timeout
                	self.ser = serial.Serial(port=port_number, baudrate=57600, timeout=1)
                except:
                        print "dmx_usb.__init__: ERROR: Could not open COM%u" % (port_number+1)
                        #sys.exit(0)
                else:
                	print "dmx_usb.__init__: Using %s" % (ser.portstr)

        # Low level functions (for inside use only)
        def transmit(self, label, data, data_size):
        	self.ser.write(chr(SOM_VALUE))
        	self.ser.write(chr(label))
        	self.ser.write(chr(data_size & 0xFF))
        	self.ser.write(chr((data_size >> 8) & 0xFF))
        	for j in range(data_size):
        		self.ser.write(data[j])
        	self.ser.write(chr(EOM_VALUE))

        # Higher level functions:
        def set_channel(self, channel, value=0):
                # Channel = DMX Channel (1-512)
                # Value = Strength (0-100%)
                self.channels[channel] = value
                self.update_channels()

        def update_channels(self):
                '''Send all 512 DMX Channels from channels[] to the hardware:
                update_channels()'''
                # This is where the magic happens
                print "dmx_usb.update_channels: Updating....."
                self.int_data = [0] + self.channels
                self.msg_data = [chr(self.int_data[j]) for j in range(len(self.int_data))]
                #self.transmit(self.OUTPUT_ONLY_SEND_DMX_LABEL, self.msg_data, len(self.msg_data))

        def close_serial(self):
                self.ser.close()

        def dmx_test(self, start=1, finish=512):
                print "dmx_usb.dmx_test: Starting DMX test"
                print "dmx_usb.dmx_test: Testing range " + str(start) + " to " + str(finish)
                for i in range(start, finish):
                        print "dmx_usb.dmx_test: Test channel " + str(i)
                        self.set_channel(i, 100)
                        time.sleep(1)
                        self.set_channel(i, 0)
                print "dmx_usb.dmx_test: Test Complete!"
                print "dmx_usb.dmx_test: Tested " + str(finish-start+1) + " channels, from " +str(start)+ " to " + str(finish)

        def blackout(self):
                channels = [0 for i in range(512)]
                self.update_channels()


# Start
print "'dmx_usb' test:"
print "  Create new object"
print "  dmx = pydmx()"
dmx = pydmx()
print
print "  Blackout:"
print "  pydmx.blackout()"
dmx.blackout()
print
print "  Set channel 1 to 100% (recommended way)"
print "  pydmx.set_channel(1,100)"
dmx.set_channel(1,100)
print
print "  Force update of channels"
print "  pydmx.update_channels()"
dmx.update_channels()
print
print "  DMX Test (1 - 18): "
print "  pydmx.dmx_test(1, 18)"
dmx.dmx_test(1,18)
print 
