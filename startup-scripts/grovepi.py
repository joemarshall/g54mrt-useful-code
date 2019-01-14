# grovepi.py
# v1.5, with Joe M additions
# This file provides the basic functions for using the GrovePi
#
# Joe M: added things to a)make it faster, and b)do retries when i2c fails, as it seems to do sometimes,
#        especially with fewer delays. Oh, and pydoc
#
# Karan Nayan, Joe Marshall
# Initial Date: 13 Feb 2014
# Last Updated: 10 Jan 2017
# 
#
# http://www.dexterindustries.com/
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
################################################################################################################
import smbus
import time
import math
import RPi.GPIO as GPIO
import struct
import sys


debug=False

if sys.version_info<(3,0):
    p_version=2
else:
    p_version=3

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1) 
else:
    bus = smbus.SMBus(0) 

#I2C Address of Arduino
address = 0x04

#Command Format
dRead_cmd=[1]   #digitalRead() command format header
dWrite_cmd=[2]  #digitalWrite() command format header 
aRead_cmd=[3]   #analogRead() command format header
aWrite_cmd=[4]  #analogWrite() command format header
pMode_cmd=[5]   #pinMode() command format header
uRead_cmd=[7]   #Ultrasonic read
# Get firmware version
version_cmd = [8]
acc_xyz_cmd=[20]    #Accelerometer (+/- 1.5g) read
rtc_getTime_cmd=[30]    #RTC get time
dht_temp_cmd=[40]   #DHT Pro sensor temperature

pulse_read_cmd=[23]


unused = 0
retries = 10

#Function declarations of the various functions used for encoding and sending data from RPi to Arduino
# Write I2C block
def write_i2c_block(address, block):
    """ Write I2C block, used internally only """
    for i in range(retries):
        try:
            return bus.write_i2c_block_data(address, 1, block)
        except IOError:
            if debug:
                print ("IOError")
    return -1

# Read I2C byte
def read_i2c_byte(address):
    """ Read I2C byte, used internally only """
    for i in range(retries):
        try:
            return bus.read_byte(address)
        except IOError:
            if debug:
                print ("IOError")
    return -1


# Read I2C block
def read_i2c_block(address):
    """ Read I2C block, used internally only """
    for i in range(retries):
        try:
            return bus.read_i2c_block_data(address, 1)
        except IOError:
            if debug:
                print ("IOError")
    return -1

def digitalRead(pin):
    """ Arduino Digital Read from digital pin <pin>"""
    write_i2c_block(address, dRead_cmd + [pin, unused, unused])
    # time.sleep(.1)
    n = read_i2c_byte(address)
    return n

# Arduino Digital Write
def digitalWrite(pin, value):
    """ Arduino Digital write to digital pin <pin>"""
    write_i2c_block(address, dWrite_cmd + [pin, value, unused])
    return 1
    
def version():
    """ Read the firmware version from the GrovePI board """
    write_i2c_block(address, version_cmd + [unused, unused, unused])
    time.sleep(.1)
    read_i2c_byte(address)
    number = read_i2c_block(address)
    return "%s.%s.%s" % (number[1], number[2], number[3])

    
#Setting Up Pin mode on Arduino
def pinMode(pin, mode):
    """ Arduino set pin mode for digital pin <pin>
    
        Don't mess with this - if you set a pin as output, and connect a sensor to it, bad things can happen.
    
        Args:
            pin:
                The pin to set the output mode on
            mode:
                One of "OUTPUT" or "INPUT", as to whether this pin is an output or an input.
    """
    if mode == "OUTPUT":
        write_i2c_block(address, pMode_cmd + [pin, 1, unused])
    elif mode == "INPUT":
        write_i2c_block(address, pMode_cmd + [pin, 0, unused])
    return 1
        

# Read analog value from Pin
def analogRead(pin):
    """ Read analog value from analog pin <pin> """
    write_i2c_block(address, aRead_cmd + [pin, unused, unused])
    read_i2c_byte(address)
    number = read_i2c_block(address)
    return number[1] * 256 + number[2]


# Write PWM
def analogWrite(pin, value):
    """ Write PWM on digital pin <pin> """
    write_i2c_block(address, aWrite_cmd + [pin, value, unused])
    return 1
                     
def temp(pin,model = '1.0'):
    """ Read temp from Grove Temp Sensor """
    # each of the sensor revisions use different thermistors, each with their own B value constant
    if model == '1.2':
        bValue = 4250  # sensor v1.2 uses thermistor ??? (assuming NCP18WF104F03RC until SeeedStudio clarifies)
    elif model == '1.1':
        bValue = 4250  # sensor v1.1 uses thermistor NCP18WF104F03RC
    else:
        bValue = 3975  # sensor v1.0 uses thermistor TTC3A103*39H
    a = analogRead(pin)
    resistance = (float)(1023 - a) * 10000 / a
    t = (float)(1 / (math.log(resistance / 10000) / bValue + 1 / 298.15) - 273.15)
    return t
    
def ultrasonicRead(pin):
    """ Read value from Grove Ultrasonic sensor """
    write_i2c_block(address, uRead_cmd + [pin, unused, unused])
    time.sleep(.06) #firmware has a time of 50ms so wait for more than that
    read_i2c_byte(address)
    number = read_i2c_block(address)
    return (number[1] * 256 + number[2])

    
def ultrasonicReadBegin(pin):
    """ Start to read value from Grove Ultrasonic sensor - you can't do other grovepi things before doing ultrasonicReadFinish, but you can read accelerometer, nfc etc. """
    write_i2c_block(address,uRead_cmd+[pin,0,0])
    return 0

def ultrasonicReadFinish(pin):
    """ Finish reading value from Grove Ultrasonic sensor - you can't do other grovepi things between ultrasonicReadBegin and ultrasonicReadFinish, but you can read accelerometer, nfc etc. """
    read_i2c_byte(address)
    number = read_i2c_block(address) 
    return (number[1]*256+number[2])
        
        
def acc_xyz():
    """ Read Grove Accelerometer (+/- 1.5g) XYZ value """
    write_i2c_block(address,acc_xyz_cmd+[0,0,0])
    time.sleep(.1)
    read_i2c_byte(address)
    number = read_i2c_block(address)
    if number[1]>32:
        number[1]=-(number[1]-224)
    if number[2]>32:
        number[2]=-(number[2]-224)
    if number[3]>32:
        number[3]=-(number[3]-224)
    return (number[1],number[2],number[3])
   

def rtc_getTime():
    """ Read from Grove RTC"""
    write_i2c_block(address,rtc_getTime_cmd+[0,0,0])
    time.sleep(.1)
    read_i2c_byte(address)
    number = read_i2c_block(address)
    return number


def dht(pin,module_type):
    """ Read and return temperature and humidity from Grove DHT Pro """
    for retries in range(5):
        try:
            write_i2c_block(address, dht_temp_cmd + [pin, module_type, unused])

            # Delay necessary for proper reading fron DHT sensor
            # time.sleep(.6)
            try:
                read_i2c_byte(address)
                number = read_i2c_block(address)
                # time.sleep(.1)
                if number == -1:
                    return [-1,-1]
            except (TypeError, IndexError):
                return [-1,-1]
            # data returned in IEEE format as a float in 4 bytes
            
            if p_version==2:
                h=''
                for element in (number[1:5]):
                    h+=chr(element)
                    
                t_val=struct.unpack('f', h)
                t = round(t_val[0], 2)

                h = ''
                for element in (number[5:9]):
                    h+=chr(element)
                
                hum_val=struct.unpack('f',h)
                hum = round(hum_val[0], 2)
            else:
                t_val=bytearray(number[1:5])
                h_val=bytearray(number[5:9])
                t=round(struct.unpack('f',t_val)[0],2)
                hum=round(struct.unpack('f',h_val)[0],2)
            if t > -100.0 and t <150.0 and hum >= 0.0 and hum<=100.0:
                return [t, hum]
            else:
                return [float('nan'),float('nan')]        
        except IOError:
            pass
    print ("Error, couldn't read DHT 5 times")
    return [-1,1]

_read_heart=False    
# get heartbeat and check if a beat has happened from the pulse sensor amped
# returns [beathappened (true or false),current BPM] bpm zero = no pulse detected
def heartRead(pin):
    global _read_heart
    if not _read_heart:
        if version()<[1,2,8]:
            print("You need updated firmware for heart rate sensor")
            return [-1,-1]
    _read_heart=True
    write_i2c_block(address,pulse_read_cmd+[pin,unused,unused])
    data_back=read_i2c_block(address)[0:4]
    if data_back[0]!=255:
      return [data_back[1]==1,data_back[3]*256+data_back[2]]
    else:
      return [-1,-1]
    