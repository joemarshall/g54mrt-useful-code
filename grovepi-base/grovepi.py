# grovepi.py
# Based on old grovepi versions
# Works with firmware 1.4.0 (and 1.2.7 in theory)
# This file provides the basic functions for using the GrovePi
#
# Joe M: added things to a)make it faster, and b)do retries when i2c fails, as it seems to do sometimes,
#        especially with fewer delays. Oh, and pydoc
#
# Karan Nayan, Joe Marshall
# Initial Date: 13 Feb 2014
# Last Updated: 14 Jan 2022
# 
#
# http://www.dexterindustries.com/
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
################################################################################################################
import smbus2 as smbus
import time
import math
import RPi.GPIO as GPIO
import struct
import sys

gpVersion=None
debug=False

if sys.version_info<(3,0):
    p_version=2
else:
    p_version=3

bus=None
def resetBus(retries):
    global bus
    if bus!=None:
        bus.close()
        bus=None
        # if we have a lot of retries then sleep so that bus definitely gets closed properly
        if retries>=5: 
            time.sleep(0.1)
    rev = GPIO.RPI_REVISION
    if rev > 1:
        bus = smbus.SMBus(1) 
    else:
        bus = smbus.SMBus(0) 

def closeBus():
    global bus
    if bus!=None:
        bus.close()
        bus=None

resetBus(0)

data_not_available_cmd=23

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
def write_i2c_block(block):
    """ Write I2C block, used internally only """
    if bus==None:
        resetBus(-1)
    for i in range(retries):
        try:
            return bus.write_i2c_block_data(address, 1,block)
        except IOError:
            resetBus(i)
            if debug:
                print ("IOError write_i2c_block")
    if debug:
        print ("fail write_i2c_block")
    return -1

# Read I2C byte
def read_i2c_byte():
    """ Read I2C byte, used internally only """
    if bus==None:
        resetBus(-1)
    for i in range(retries):
        try:
            return bus.read_byte(address)
        except IOError:
            resetBus(i)
            if debug:
                print ("IOError")
    if debug:
        print ("fail READ_i2c_byte")
    return -1


# Read I2C write_i2c_block
def read_i2c_block(no_bytes):
    """ Read I2C block, used internally only """
    if bus==None:
        resetBus(-1)    
    for i in range(retries):
        try:
            msg=smbus.i2c_msg.read(address,no_bytes)
            bus.i2c_rdwr(msg)
            retVal=[]
            for c in range(no_bytes):
                retVal.append(ord(msg.buf[c]))
            if retVal[0] == data_not_available_cmd and debug:
                print("Not available yet")
                continue
            return retVal
        except IOError:
            resetBus(i)
            if debug:
                print ("IOError read_i2c_block")
    if debug:
        print ("fail READ_i2c_block")
    return [data_not_available_cmd]
    
def read_identified_i2c_block(read_command_id, no_bytes):
    global gpVersion,address
    if gpVersion<[1,4,0]:
#        print("OLD")
        data=read_i2c_block(no_bytes+1)
#        print(data,no_bytes)
    else:
#        print("NEW")
        data=[-1]
        while data[0]!=read_command_id[0]:
            data=read_i2c_block(no_bytes+1)
    return data[1:]

def digitalRead(pin):
    """ Arduino Digital Read from digital pin <pin>"""
    if bus==None:
        resetBus(-1)
    write_i2c_block(dRead_cmd + [pin, unused, unused])    
    if gpVersion<[1,4,0]:
        data= bus.read_byte(address)
    else:
        data = read_identified_i2c_block( dRead_cmd, no_bytes = 1)[0]
    return data

# Arduino Digital Write
def digitalWrite(pin, value):
    """ Arduino Digital write to digital pin <pin>"""
    write_i2c_block(dWrite_cmd + [pin, value, unused])
    read_i2c_block(1)
    return 1
    
def versionList():    
    """ Read the firmware version from the GrovePI board """
    for i in range(retries):
        try:
            write_i2c_block(version_cmd+[unused,unused,unused])
            time.sleep(.1)
            values=read_i2c_block(4)
            vCmd=values[0]
            number=values
            return number[1:]
        except IOError:
            resetBus(i)
            if debug:
                print ("IOError")
    return [-1,-1,-1]
    
def version():
    """ Read the firmware version from the GrovePI board """
    if bus==None:
        resetBus(-1)
    for i in range(retries):
        try:
            bus.write_i2c_block_data(address,1, version_cmd + [unused, unused, unused])
            time.sleep(.1)
            bus.read_byte(address)
            number = bus.read_i2c_block_data(address,1,4)
            return "%s.%s.%s" % (number[1], number[2], number[3])
        except IOError:
            resetBus(i)
            if debug:
                print ("IOError")
    return "-1.-1.-1"

    
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
        write_i2c_block(pMode_cmd + [pin, 1, unused])
    elif mode == "INPUT":
        write_i2c_block(pMode_cmd + [pin, 0, unused])
    read_i2c_block(no_bytes = 1)        
    return 1
        

# Read analog value from Pin
def analogRead(pin):
    """ Read analog value from analog pin <pin> """ 
    write_i2c_block(aRead_cmd + [pin, unused, unused])
    number = read_identified_i2c_block(aRead_cmd, no_bytes = 2)
    return number[0] * 256 + number[1]

# Write PWM
def analogWrite(pin, value):
    """ Write PWM on digital pin <pin> """
    write_i2c_block(aWrite_cmd + [pin, value, unused])
    read_i2c_block(no_bytes = 1)
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
    write_i2c_block(uRead_cmd + [pin, unused, unused])
    if gpVersion<[1,4,0]:
        time.sleep(.06)#firmware has a time of 50ms so wait for more than that

    number = read_identified_i2c_block(uRead_cmd, no_bytes = 2)
    return (number[0] * 256 + number[1])

    
def ultrasonicReadBegin(pin):
    """ Start to read value from Grove Ultrasonic sensor - you can't do other grovepi things before doing ultrasonicReadFinish, but you can read accelerometer, nfc etc. """
    write_i2c_block(uRead_cmd+[pin,0,0])
    return 0

def ultrasonicReadFinish(pin):
    """ Finish reading value from Grove Ultrasonic sensor - you can't do other grovepi things between ultrasonicReadBegin and ultrasonicReadFinish, but you can read accelerometer, nfc etc. Returns -1 if not ready """
    number = read_i2c_block(3) 
    if number[0]==uRead_cmd:
        return (number[1]*256+number[2])
    else:
        return -1
        
           

_PREV_DHT={}
_PREV_DHT_TIME=time.time()        
_PREV_DHT_PIN=-1

def dht(pin,module_type=0):
    global _PREV_DHT,_PREV_DHT_TIME,_PREV_DHT_PIN
    retVal=_PREV_DHT.get(pin,[0,0])
    """ Read and return temperature and humidity from Grove DHT Pro """
    for retries in range(5):
        write_i2c_block(dht_temp_cmd + [pin, module_type, unused])
        if gpVersion<[1,4,0]:
            # old firmware needs you to pause on first reading of new pin
            # new firmware (1.4) just reads slowly always
            curTime=time.time()
            if _PREV_DHT_PIN!=pin:
                time.sleep(0.6)
            _PREV_DHT_PIN=pin
        number = read_identified_i2c_block(dht_temp_cmd, no_bytes = 8)
        #print(number)
        if p_version==2:
            h=''
            for element in (number[0:4]):
                h+=chr(element)

            t_val=struct.unpack('f', h)
            t = round(t_val[0], 2)

            h = ''
            for element in (number[4:8]):
                h+=chr(element)

            hum_val=struct.unpack('f',h)
            hum = round(hum_val[0], 2)
        else:
            t_val=bytearray(number[0:4])
            h_val=bytearray(number[4:8])
            t=round(struct.unpack('f',t_val)[0],2)
            hum=round(struct.unpack('f',h_val)[0],2)
        if t > -100.0 and t <150.0 and hum > 0.0 and hum<=100.0:
            _PREV_DHT[pin]=[t, hum]
            return [t, hum]
        else:
            return retVal
            if debug:
                print("DHT retry")
            continue
    if debug==True:
        print("Read DHT fail")
    return retVal

    
gpVersion=versionList()
