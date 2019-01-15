#!/usr/bin/python3
# -*- coding: ascii -*-

import time,sys,struct
from math import *


_DIGITAL_LIGHT_ADDR=0x29

# Commands
_CMD       = 0x80
_CMD_CLEAR = 0x40
_CMD_WORD  = 0x20
_CMD_BLOCK = 0x10

# Registers
_REG_CONTROL   = 0x80
_REG_TIMING    = 0x81
_REG_INTERRUPT = 0x86
_REG_ID        = 0x8A
_REG_BLOCKREAD = 0x8B
_REG_DATA0     = 0x8C
_REG_DATA1     = 0x8E

# Control parameters
_POWER_UP   = 0x03
_POWER_DOWN = 0x00

# Timing parameters
_GAIN_LOW          = 0b00000000
_GAIN_HIGH         = 0b00010000
_INTEGRATION_START = 0b00001000
_INTEGRATION_STOP  = 0b00000000
_INTEGRATE_13      = 0b00000000
_INTEGRATE_101     = 0b00000001
_INTEGRATE_402     = 0b00000010
_INTEGRATE_DEFAULT = _INTEGRATE_402
_INTEGRATE_NA      = 0b00000011


import smbus

bus=smbus.SMBus(1)



def _writeReg(reg,val):
    bus.write_byte(_DIGITAL_LIGHT_ADDR,reg)
    bus.write_byte(_DIGITAL_LIGHT_ADDR,val)

def _readReg(reg):
    bus.write_byte(_DIGITAL_LIGHT_ADDR,reg)
    return bus.read_byte(_DIGITAL_LIGHT_ADDR)
    
def _readWord(reg):
    bus.write_byte(_DIGITAL_LIGHT_ADDR,reg)
    low=bus.read_byte(_DIGITAL_LIGHT_ADDR)
    bus.write_byte(_DIGITAL_LIGHT_ADDR,reg+1)
    high=bus.read_byte(_DIGITAL_LIGHT_ADDR)
    return 256*high+low
    
def _initSensor():
#    bus.write_byte_data(_DIGITAL_LIGHT_ADDR,0,0x0)
#    time.sleep(.5)

    # power on
    _writeReg(_REG_CONTROL,0x3)
    time.sleep(0.5)
    print("Power:",_readReg(_REG_CONTROL))
#    # timing - sample every 13 ms
    _writeReg(_REG_TIMING,0x11)
    
    _writeReg(_REG_CONTROL,0x3)
    _writeReg(_REG_INTERRUPT,0x0)
    print ("ID:%x"%_readReg(_REG_ID))
    
_initSensor()

def getSensorValues(gain=16):
#    _writeReg(_REG_CONTROL,0x3)
    if gain==16:
        _writeReg(_REG_TIMING,0x11)
    else:
        _writeReg(_REG_TIMING,0x01)    
 #   time.sleep(0.114)
    data0=_readWord(_REG_DATA0)
    data1=_readWord(_REG_DATA1)
    return data0,data1

LUX_SCALE=14           # scale by 2^14
RATIO_SCALE=9          # scale ratio by 2^9
CH_SCALE= 10            # scale channel values by 2^10
CHSCALE_TINT0= 0x7517   # 322/11 * 2^CH_SCALE
CHSCALE_TINT1= 0x0fe7   # 322/81 * 2^CH_SCALE    
        
K1T=0x0040   # 0.125 * 2^RATIO_SCALE
B1T=0x01f2   # 0.0304 * 2^LUX_SCALE
M1T=0x01be   # 0.0272 * 2^LUX_SCALE
K2T=0x0080   # 0.250 * 2^RATIO_SCA
B2T=0x0214   # 0.0325 * 2^LUX_SCALE
M2T=0x02d1   # 0.0440 * 2^LUX_SCALE
K3T=0x00c0   # 0.375 * 2^RATIO_SCALE
B3T=0x023f   # 0.0351 * 2^LUX_SCALE
M3T=0x037b   # 0.0544 * 2^LUX_SCALE
K4T=0x0100   # 0.50 * 2^RATIO_SCALE
B4T=0x0270   # 0.0381 * 2^LUX_SCALE
M4T=0x03fe   # 0.0624 * 2^LUX_SCALE
K5T=0x0138   # 0.61 * 2^RATIO_SCALE
B5T=0x016f   # 0.0224 * 2^LUX_SCALE
M5T=0x01fc   # 0.0310 * 2^LUX_SCALE
K6T=0x019a   # 0.80 * 2^RATIO_SCALE
B6T=0x00d2   # 0.0128 * 2^LUX_SCALE
M6T=0x00fb   # 0.0153 * 2^LUX_SCALE
K7T=0x029a   # 1.3 * 2^RATIO_SCALE
B7T=0x0018   # 0.00146 * 2^LUX_SCALE
M7T=0x0012   # 0.00112 * 2^LUX_SCALE
K8T=0x029a   # 1.3 * 2^RATIO_SCALE
B8T=0x0000   # 0.000 * 2^LUX_SCALE
M8T=0x0000   # 0.000 * 2^LUX_SCALE        
        
def getLux(gain=1,val0=None,val1=None):
    if val0==None:
        val0,val1=getSensorValues(gain)
    chScale=CHSCALE_TINT1 # if we are getting values every 100ms
#        chScale=CHSCALE_TINT0 # if we are getting values every 13ms, which we are
    if gain!=16:
        chScale = chScale << 4 
    channel0 = (val0 * chScale) >> CH_SCALE
    channel1 = (val1 * chScale) >> CH_SCALE
    ratio1 = 0
    if channel0!= 0:
        ratio1 = (channel1 << (RATIO_SCALE+1))/channel0
    # round the ratio value
    ratio = (int)((ratio1 + 1) >> 1)
    
    if (ratio >= 0) and (ratio <= K1T):
        b=B1T
        m=M1T
    elif ratio <= K2T:
        b=B2T
        m=M2T
    elif ratio <= K3T:
        b=B3T
        m=M3T
    elif ratio <= K4T:
        b=B4T
        m=M4T
    elif ratio <= K5T:
        b=B5T
        m=M5T
    elif ratio <= K6T:
        b=B6T
        m=M6T
    elif ratio <= K7T:
        b=B7T
        m=M7T
    else:
        b=B8T
        m=M8T
    temp=((channel0*b)-(channel1*m));
    if temp<0:
        temp=0;
    temp+=(1<<(LUX_SCALE-1))
    lux=temp>>LUX_SCALE;
    return lux    
    
if __name__=="__main__":
    while True:
        print( "%d,%d"%getSensorValues())
#        print getLux(1),getLux(16)
#        time.sleep(0.5)
