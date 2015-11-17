#!/usr/bin/python3
# -*- coding: ascii -*-
"""
    Reads from the grove color sensor (TCS3404)

    example code:
        # get red, green, blue, clear values from sensor
        (r,g,b,c)=grovecolor.getRGBC()
        print (r,g,b,c)
        
"""

import smbus

COLOR_SENSOR_ADDR=0x39

REG_CTL=0x80
REG_TIMING=0x81
REG_INT=0x82
REG_INT_SOURCE=0x83
REG_ID=0x84
REG_GAIN=0x87
REG_LOW_THRESH_LOW_BYTE=0x88
REG_LOW_THRESH_HIGH_BYTE=0x89
REG_HIGH_THRESH_LOW_BYTE=0x8A
REG_HIGH_THRESH_HIGH_BYTE=0x8B
#The REG_BLOCK_READ and REG_GREEN_LOW direction are the same
REG_BLOCK_READ=0xD0 
REG_GREEN_LOW=0xD0
REG_GREEN_HIGH=0xD1
REG_RED_LOW=0xD2
REG_RED_HIGH=0xD3
REG_BLUE_LOW=0xD4
REG_BLUE_HIGH=0xD5
REG_CLEAR_LOW=0xD6
REG_CLEAR_HIGH=0xD7
CTL_DAT_INITIATE=0x03
CLR_INT=0xE0

#Timing Register
SYNC_EDGE=0x40
INTEG_MODE_FREE=0x00
INTEG_MODE_MANUAL=0x10
INTEG_MODE_SYN_SINGLE=0x20
INTEG_MODE_SYN_MULTI=0x30
 
INTEG_PARAM_PULSE_COUNT1=0x00
INTEG_PARAM_PULSE_COUNT2=0x01
INTEG_PARAM_PULSE_COUNT4=0x02
INTEG_PARAM_PULSE_COUNT8=0x03

#Interrupt Control Register 
INTR_STOP=40
INTR_DISABLE=0x00
INTR_LEVEL=0x10
INTR_PERSIST_EVERY=0x00
INTR_PERSIST_SINGLE=0x01

#Interrupt Souce Register
INT_SOURCE_GREEN=0x00
INT_SOURCE_RED=0x01
INT_SOURCE_BLUE=0x10
INT_SOURCE_CLEAR=0x03

#Gain Register
GAIN_1=0x00
GAIN_4=0x10
GAIN_16=0x20
GAIN_64=0x30
PRESCALER_1=0x00
PRESCALER_2=0x01
PRESCALER_4=0x02
PRESCALER_8=0x03
PRESCALER_16=0x04
PRESCALER_32=0x05
PRESCALER_64=0x06



bus=smbus.SMBus(1)

def _initSensor():
    # set something to do with timing
    bus.write_byte_data(COLOR_SENSOR_ADDR,REG_TIMING,INTEG_MODE_FREE | INTEG_PARAM_PULSE_COUNT1) #get data as fast as the chip wants to
    bus.write_byte_data(COLOR_SENSOR_ADDR,REG_INT_SOURCE,INT_SOURCE_CLEAR) # fire interrupt once clear signal is loaded
    bus.write_byte_data(COLOR_SENSOR_ADDR,REG_INT,INTR_LEVEL | INTR_PERSIST_EVERY) # interrupt every time round (ignored I think)
    bus.write_byte_data(COLOR_SENSOR_ADDR,REG_GAIN,GAIN_64 | PRESCALER_4) # set scaling of the data
    bus.write_byte_data(COLOR_SENSOR_ADDR,REG_CTL,CTL_DAT_INITIATE)    # turn on the sensor readings

_initSensor()
    
def getRGBC():
    r=bus.read_byte_data(COLOR_SENSOR_ADDR,REG_RED_LOW)
    r+=256*bus.read_byte_data(COLOR_SENSOR_ADDR,REG_RED_HIGH)
    g=bus.read_byte_data(COLOR_SENSOR_ADDR,REG_GREEN_LOW)
    g+=256*bus.read_byte_data(COLOR_SENSOR_ADDR,REG_GREEN_HIGH)
    b=bus.read_byte_data(COLOR_SENSOR_ADDR,REG_BLUE_LOW)
    b+=256*bus.read_byte_data(COLOR_SENSOR_ADDR,REG_BLUE_HIGH)
    c=bus.read_byte_data(COLOR_SENSOR_ADDR,REG_CLEAR_LOW)
    c+=256*bus.read_byte_data(COLOR_SENSOR_ADDR,REG_CLEAR_HIGH)
    return (r,g,b,c)


if __name__=="__main__":
    while True:
        (r,g,b,c)=getRGBC()
        print "Color Sensor RGBC:",(r,g,b,c)
