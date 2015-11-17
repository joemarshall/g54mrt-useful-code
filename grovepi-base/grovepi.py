# grovepi.py
# v1.1, with Joe M additions
# This file provides the basic functions for using the GrovePi
#
# Joe M: added things to a)make it faster, and b)do retries when i2c fails, as it seems to do sometimes,
#        especially with fewer delays. Oh, and pydoc
#
# Karan Nayan, Joe Marshall
# Initial Date: 13 Feb 2014
# Last Updated: 23 Sep 2014
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
acc_xyz_cmd=[20]    #Accelerometer (+/- 1.5g) read
rtc_getTime_cmd=[30]    #RTC get time
dht_temp_cmd=[40]   #DHT Pro sensor temperature

#Function declarations of the various functions used for encoding and sending data from RPi to Arduino


def write_i2c_block(address,block):
    """ Write I2C block, used internally only """
    return bus.write_i2c_block_data(address,1,block)


def read_i2c_byte(address):
    """ Read I2C byte, used internally only """
    return bus.read_byte(address)


def read_i2c_block(address):
    """ Read I2C block, used internally only """
    return bus.read_i2c_block_data(address,1)

def digitalRead(pin):
    """ Arduino Digital Read from digital pin <pin>"""
    for retries in range(5):
        try:
            write_i2c_block(address,dRead_cmd+[pin,0,0])
            time.sleep(.01)
            n=read_i2c_byte(address)
            return n
        except IOError:
            time.sleep(.01)
    print("IOError digital read")
    return -1

def digitalWrite(pin,value):
    """ Arduino Digital write to digital pin <pin>"""
    for retries in range(5):
        try:
            write_i2c_block(address,dWrite_cmd+[pin,value,0])
            return 1
        except IOError:
            time.sleep(0.01)
    return -1

#Setting Up Pin mode on Arduino
def pinMode(pin,mode):
    """ Arduino set pin mode for digital pin <pin>
    
        Don't mess with this - if you set a pin as output, and connect a sensor to it, bad things can happen.
    
        Args:
            pin:
                The pin to set the output mode on
            mode:
                One of "OUTPUT" or "INPUT", as to whether this pin is an output or an input.
    """
    try:
        if mode == "OUTPUT":
            write_i2c_block(address,pMode_cmd+[pin,1,0])
        elif mode == "INPUT":
            write_i2c_block(address,pMode_cmd+[pin,0,0])
        return 1
    except IOError:
        print("IOError")
        return -1
        
#Read analog value from Pin
def analogRead(pin):
    """ Read analog value from analog pin <pin> """
    for retries in range(5):
        try:
            bus.write_i2c_block_data(address,1,aRead_cmd+[pin,0,0])
            time.sleep(.01)
            bus.read_byte(address)
            number = bus.read_i2c_block_data(address,1)
            return number[1]*256+number[2]
        except IOError:
            pass
    print("IOError analog read")
    return -1

def analogWrite(pin,value):
    """ Write PWM on digital pin <pin> """
        
    try:
        write_i2c_block(address,aWrite_cmd+[pin,value,0])
        return 1
    except IOError:
        print("IOError")
        return -1

def temp(pin):
    """ Read temp from Grove Temp Sensor """
    try:
        a=analogRead(pin)
        resistance=(float)(1023-a)*10000/a
        t=(float)(1/(math.log(resistance/10000)/3975+1/298.15)-273.15) 
        return t
    except IOError:
        print("IOError")
        return -1

def ultrasonicRead(pin):
    """ Read value from Grove Ultrasonic sensor """
    for retries in range(5):
        try:
            write_i2c_block(address,uRead_cmd+[pin,0,0])
            time.sleep(.06)
            read_i2c_byte(address)
            number = read_i2c_block(address) 
            return (number[1]*256+number[2])
        except IOError:
            pass
    print("IOError ultrasonic read")
    return -1
        
def ultrasonicReadBegin(pin):
    """ Start to read value from Grove Ultrasonic sensor - you can't do other grovepi things before doing ultrasonicReadFinish, but you can read accelerometer, nfc etc. """
    for retries in range(5):
        try:
            write_i2c_block(address,uRead_cmd+[pin,0,0])
            return 0
        except IOError:
            pass
    print("IOError ultrasonic read")
    return -1

def ultrasonicReadFinish(pin):
    """ Finish reading value from Grove Ultrasonic sensor - you can't do other grovepi things between ultrasonicReadBegin and ultrasonicReadFinish, but you can read accelerometer, nfc etc. """
    for retries in range(5):
        try:
            read_i2c_byte(address)
            number = read_i2c_block(address) 
            return (number[1]*256+number[2])
        except IOError:
            pass
    print("IOError ultrasonic read")
    return -1         
        
        
def acc_xyz():
    """ Read Grove Accelerometer (+/- 1.5g) XYZ value """
    try:
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
    except IOError:
        print("IOError")
        return None
   

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
            write_i2c_block(address,dht_temp_cmd+[pin,module_type,0])

            #Delay necessary for proper reading fron DHT sensor
            time.sleep(.6) 
            try:
                read_i2c_byte(address)
                number = read_i2c_block(address)
                if number==-1:
                    return -1
            except (TypeError,IndexError):
                return -1
            #data returned in IEEE format as a float in 4 bytes 
            f=0

            for element in reversed(number[1:5]):   #data is reversed 
                hex_val=hex(element)    #Converted to hex
                #print hex_val
                try:
                    h_val=hex_val[2]+hex_val[3]
                except IndexError:
                    h_val='0'+hex_val[2]
                if f==0:    #Convert to char array
                    h=h_val
                    f=1
                else:
                    h=h+h_val
            t=round(struct.unpack('!f', h.decode('hex'))[0],2)#convert the temp back to float

            h=''
            for element in reversed(number[5:9]):   #data is reversed 
                hex_val=hex(element)    #Converted to hex
                #print hex_val
                try:
                    h_val=hex_val[2]+hex_val[3]
                except IndexError:
                    h_val='0'+hex_val[2]
                if f==0:    #Convert to char array
                    h=h_val
                    f=1
                else:
                    h=h+h_val
            hum=round(struct.unpack('!f', h.decode('hex'))[0],2)#convert back to float
            return [t,hum]
        except IOError:
            pass
    print "Error, couldn't read DHT 5 times"
    return -1
