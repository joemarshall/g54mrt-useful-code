#!/usr/bin/python3
# -*- coding: ascii -*-

import time,sys,struct
from math import *


X_AXIS=0
Y_AXIS=1
Z_AXIS=2

# LSM303 Register definitions 
CTRL_REG1_A=0x20
CTRL_REG2_A=0x21
CTRL_REG3_A=0x22
CTRL_REG4_A=0x23
CTRL_REG5_A=0x24
HP_FILTER_RESET_A=0x25
REFERENCE_A=0x26
STATUS_REG_A=0x27
OUT_X_L_A=0x28
OUT_X_H_A=0x29
OUT_Y_L_A=0x2A
OUT_Y_H_A=0x2B
OUT_Z_L_A=0x2C
OUT_Z_H_A=0x2D
INT1_CFG_A=0x30
INT1_SOURCE_A=0x31
INT1_THS_A=0x32
INT1_DURATION_A=0x33
CRA_REG_M=0x00
CRB_REG_M=0x01#refer to the Table 58 of the datasheet of LSM303DLM
MAG_SCALE_1_3=0x20#full-scale is +/-1.3Gauss
MAG_SCALE_1_9=0x40#+/-1.9Gauss
MAG_SCALE_2_5=0x60#+/-2.5Gauss
MAG_SCALE_4_0=0x80#+/-4.0Gauss
MAG_SCALE_4_7=0xa0#+/-4.7Gauss
MAG_SCALE_5_6=0xc0#+/-5.6Gauss
MAG_SCALE_8_1=0xe0#+/-8.1Gauss
MR_REG_M=0x02
OUT_X_H_M=0x03
OUT_X_L_M=0x04
OUT_Y_H_M=0x07
OUT_Y_L_M=0x08
OUT_Z_H_M=0x05
OUT_Z_L_M=0x06
SR_REG_M=0x09
IRA_REG_M=0x0A
IRB_REG_M=0x0B
IRC_REG_M=0x0C

SIX_AXIS_ACCEL_ADDR=0x18
SIX_AXIS_MAG_ADDR=0x1E

import smbus2 as smbus


bus=smbus.SMBus(1)
ACCEL_SCALE=2

is6axisInitialised=False

def _initv2(scale):
    global SIX_AXIS_ACCEL_ADDR
    global OUT_X_L_M
    global OUT_X_H_M
    global OUT_Y_L_M
    global OUT_Y_H_M
    global OUT_Z_L_M
    global OUT_Z_H_M
    global OUT_X_L_A
    global OUT_X_H_A
    global OUT_Y_L_A
    global OUT_Y_H_A
    global OUT_Z_L_A
    global OUT_Z_H_A
    SIX_AXIS_ACCEL_ADDR=SIX_AXIS_MAG_ADDR
    OUT_X_L_M       = 0x08
    OUT_X_H_M       = 0x09
    OUT_Y_L_M       = 0x0A
    OUT_Y_H_M       = 0x0B
    OUT_Z_L_M       = 0x0C
    OUT_Z_H_M       = 0x0D    
    OUT_X_L_A       = 0x28
    OUT_X_H_A       = 0x29
    OUT_Y_L_A       = 0x2A
    OUT_Y_H_A       = 0x2B
    OUT_Z_L_A       = 0x2C
    OUT_Z_H_A       = 0x2D
    CTRL_REG0       = 0x1F
    CTRL_REG1       = 0x20
    CTRL_REG2       = 0x21
    CTRL_REG3       = 0x22
    CTRL_REG4       = 0x23
    CTRL_REG5       = 0x24
    CTRL_REG6       = 0x25
    CTRL_REG7       = 0x26
    MAG_SCALE_2 	= 0x00 #full-scale is +/-2Gauss
    MAG_SCALE_4 	= 0x20 #+/-4Gauss
    MAG_SCALE_8 	= 0x40 #+/-8Gauss
    MAG_SCALE_12 	= 0x60 #+/-12Gauss

    ACCELE_SCALE 	= 2

    LSM303_write(0x57, CTRL_REG1)               # 0x57 = ODR=50hz, all accel axes on
    LSM303_write((3<<6)|(0<<3), CTRL_REG2)      # set full-scale
    LSM303_write(0x00, CTRL_REG3)           # no interrupt
    LSM303_write(0x00, CTRL_REG4)           # no interrupt
    LSM303_write((4<<2), CTRL_REG5)             # 0x10 = mag 50Hz output rate
    LSM303_write(MAG_SCALE_2, CTRL_REG6)        # magnetic scale = +/-1.3Gauss
    LSM303_write(0x00, CTRL_REG7)           # 0x00 = continouous conversion mode

def init6Axis(scale=2):
    global ACCEL_SCALE
    try:
        LSM303_write(0x27,CTRL_REG1_A)
    except IOError as e:
        # check for an LSM303D (different I2c interface and setup)
        _initv2(scale)
        return
    LSM303_write(0x27, CTRL_REG1_A)
    if scale==8 or scale==4:
        LSM303_write((0x00 | (fs-fs/2-1)<<4), CTRL_REG4_A) # set full-scale
        ACCEL_SCALE=scale
    else:
        LSM303_write(0x00, CTRL_REG4_A);
        ACCEL_SCALE=2    
    LSM303_write(0x14, CRA_REG_M)  # 0x14 = mag 30Hz output rate
    LSM303_write(MAG_SCALE_1_3, CRB_REG_M) #magnetic scale = +/-1.3Gauss
    LSM303_write(0x00, MR_REG_M)  # 0x00 = continouous conversion mode
    is6axisInitialised=True

def getAccel():
    """Get accelerometer values (in multiples of g)        
    """
    global is6axisInitialised
    if not is6axisInitialised:
      init6Axis()
    multiplier=ACCEL_SCALE/(2.**15.) 
    x= LSM303_readSigned16Bit(OUT_X_L_A,OUT_X_H_A)*multiplier
    y= LSM303_readSigned16Bit(OUT_Y_L_A,OUT_Y_H_A)*multiplier
    z= LSM303_readSigned16Bit(OUT_Z_L_A,OUT_Z_H_A)*multiplier
    return (x,y,z)


def getMag():
    """Get magnetometer values. 
    """
    global is6axisInitialised
    if not is6axisInitialised:
      init6Axis()
    x= LSM303_readSigned16Bit(OUT_X_L_M,OUT_X_H_M)
    y= LSM303_readSigned16Bit(OUT_Y_L_M,OUT_Y_H_M)
    z= LSM303_readSigned16Bit(OUT_Z_L_M,OUT_Z_H_M)
    return (x,y,z)
    
def getRotationMatrix(mag=None,accel=None):
    """ Returns a 3x3 matrix of how the device is rotated, based on magnetometer and accelerometer values

    Args:
        mag: Magnetometer values from getMag()
        accel: Accelerometer values from getAccel()
        
        If either argument is None, it will call getMag / getAccel
      
    Returns:
        3x3 tuple rotation matrix, put this into getOrientation(matrix) to get yaw, pitch, roll values
        or None if there isn't enough information (device is in freefall)
    """
    if mag==None:
        mag=getMag()
    if accel==None:
        accel=getAccel()
    Ax = accel[0]
    Ay = accel[1]
    Az = accel[2]
    Ex = mag[0]
    Ey = mag[1]
    Ez = mag[2]
    Hx = Ey*Az - Ez*Ay
    Hy = Ez*Ax - Ex*Az
    Hz = Ex*Ay - Ey*Ax        
    normH = sqrt(Hx*Hx + Hy*Hy + Hz*Hz)
    if normH < 0.1:
        # in freefall or something
        return None
    invH = 1.0 / normH
    Hx *= invH
    Hy *= invH
    Hz *= invH
    invA = 1.0 / sqrt(Ax*Ax + Ay*Ay + Az*Az)
    Ax *= invA;
    Ay *= invA;
    Az *= invA;
    Mx = Ay*Hz - Az*Hy;
    My = Az*Hx - Ax*Hz;
    Mz = Ax*Hy - Ay*Hx;
    return ((Hx,Hy,Hz),(Mx,My,Mz),(Ax,Ay,Az))
    
def getOrientation(matrix=None,errorValue=(0,0,0)):
    """ Get orientation values (Yaw, pitch, roll) from rotation matrix
    
    Args: 
        matrix: Rotation matrix, from getRotationMatrix(mag,accel)
                if Matrix is None, then it will call the relevant getAccel functions itself
                
        errorValue: If the rotation matrix can't be found (if it is in freefall, this value is returned. 
                    By default this is set to be just a zero value, if you want to distinguish error events
                    then set this to some other value (e.g. None)
        
    Returns:
        (yaw, pitch, roll) tuple
    """
    if matrix==None:
        matrix=getRotationMatrix()
    if matrix==None:
        return errorValue        
    yaw=atan2(matrix[0][1], matrix[1][1])
    pitch=asin(-matrix[2][1])
    roll=atan2(-matrix[2][0], matrix[2][2])
    return yaw,pitch,roll
    
def LSM303_readSigned16Bit(arg1,arg2):
    bytes=struct.pack("BB",LSM303_read(arg1),LSM303_read(arg2))
    return struct.unpack("<h",bytes)[0]

def LSM303_write(data, address):
    if address >= 0x20:
        bus.write_byte_data(SIX_AXIS_ACCEL_ADDR,address,data)
    else:
        bus.write_byte_data(SIX_AXIS_MAG_ADDR,address,data)

def LSM303_read( address):
    if address >= 0x20:
        return bus.read_byte_data(SIX_AXIS_ACCEL_ADDR,address)
    else:
        return bus.read_byte_data(SIX_AXIS_MAG_ADDR,address)
    

if __name__=="__main__":
    init6Axis()
    while True:
        print((getAccel(),getOrientation()))
        time.sleep(0.5)
