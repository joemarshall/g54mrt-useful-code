import smbus2 as smbus

import struct 
import time 
BMI088_ACC_ADDRESS         =0x19

BMI088_ACC_CHIP_ID         =0x00 
BMI088_ACC_ERR_REG         =0x02
BMI088_ACC_STATUS          =0x03

BMI088_ACC_X_LSB           =0x12
BMI088_ACC_X_MSB           =0x13
BMI088_ACC_Y_LSB           =0x14
BMI088_ACC_Y_MSB           =0x15
BMI088_ACC_Z_LSB           =0x16
BMI088_ACC_Z_MSB           =0x17

BMI088_ACC_SENSOR_TIME_0   =0x18
BMI088_ACC_SENSOR_TIME_1   =0x19
BMI088_ACC_SENSOR_TIME_2   =0x1A

BMI088_ACC_INT_STAT_1      =0x1D

BMI088_ACC_TEMP_MSB        =0x22
BMI088_ACC_TEMP_LSB        =0x23

BMI088_ACC_CONF            =0x40
BMI088_ACC_RANGE           =0x41

BMI088_ACC_INT1_IO_CTRL    =0x53
BMI088_ACC_INT2_IO_CTRL    =0x54
BMI088_ACC_INT_MAP_DATA    =0x58

BMI088_ACC_SELF_TEST       =0x6D

BMI088_ACC_PWR_CONF        =0x7C
BMI088_ACC_PWR_CTRl        =0x7D

BMI088_ACC_SOFT_RESET      =0x7E

BMI088_GYRO_ADDRESS            =0x69

BMI088_GYRO_CHIP_ID            =0x00 

BMI088_GYRO_RATE_X_LSB         =0x02
BMI088_GYRO_RATE_X_MSB         =0x03
BMI088_GYRO_RATE_Y_LSB         =0x04
BMI088_GYRO_RATE_Y_MSB         =0x05
BMI088_GYRO_RATE_Z_LSB         =0x06
BMI088_GYRO_RATE_Z_MSB         =0x07

BMI088_GYRO_INT_STAT_1         =0x0A

BMI088_GYRO_RANGE              =0x0F
BMI088_GYRO_BAND_WIDTH         =0x10

BMI088_GYRO_LPM_1              =0x11

BMI088_GYRO_SOFT_RESET         =0x14

BMI088_GYRO_INT_CTRL           =0x15
BMI088_GYRO_INT3_INT4_IO_CONF  =0x16
BMI088_GYRO_INT3_INT4_IO_MAP   =0x18

BMI088_GYRO_SELF_TEST          =0x3C

# accel range
RANGE_3G = 0x00 
RANGE_6G = 0x01 
RANGE_12G = 0x02 
RANGE_24G = 0x03 

#output data rate
ODR_12 = 0x05
ODR_25 = 0x06 
ODR_50 = 0x07 
ODR_100 = 0x08 
ODR_200 = 0x09 
ODR_400 = 0x0A 
ODR_800 = 0x0B 
ODR_1600 = 0x0C 

# gyro range
RANGE_2000 = 0x00
RANGE_1000 = 0x01 
RANGE_500 = 0x02 
RANGE_250 = 0x03 
RANGE_125 = 0x04 

#gyro out data rate
ODR_2000_BW_532 = 0x00 
ODR_2000_BW_230 = 0x01 
ODR_1000_BW_116 = 0x02 
ODR_400_BW_47 = 0x03 
ODR_200_BW_23 = 0x04 
ODR_100_BW_12 = 0x05 
ODR_200_BW_64 = 0x06 
ODR_100_BW_32 = 0x07 

#gyro power state
GYRO_NORMAL = 0x00 
GYRO_SUSPEND = 0x80 
GYRO_DEEP_SUSPEND = 0x20 


#accelerometer active or not
ACC_ACTIVE = 0x00
ACC_SUSPEND = 0x03 

_GYRO_INITED=False

bus=smbus.SMBus(1)

def init():
    global _GYRO_INITED
    _GYRO_INITED=True
    setAccScaleRange(RANGE_6G)
    setAccOutputDataRate(ODR_100)
    setAccPowerMode(ACC_ACTIVE)
    
    setGyroScaleRange(RANGE_1000)
    setGyroOutputDataRate(ODR_2000_BW_532)
    setGyroPowerMode(GYRO_NORMAL)

def setAccPowerMode(mode):
    if mode == ACC_ACTIVE:
        bus.write_byte_data(BMI088_ACC_ADDRESS, BMI088_ACC_PWR_CTRl, 0x04)
        bus.write_byte_data(BMI088_ACC_ADDRESS, BMI088_ACC_PWR_CONF, 0x00)
    elif mode == ACC_SUSPEND:
        bus.write_byte_data(BMI088_ACC_ADDRESS, BMI088_ACC_PWR_CONF, 0x03)
        bus.write_byte_data(BMI088_ACC_ADDRESS, BMI088_ACC_PWR_CTRl, 0x00)

def setGyroPowerMode(mode):
    if mode == GYRO_NORMAL:
        bus.write_byte_data(BMI088_GYRO_ADDRESS, BMI088_GYRO_LPM_1, GYRO_NORMAL)
    elif mode == GYRO_SUSPEND:
        bus.write_byte_data(BMI088_GYRO_ADDRESS, BMI088_GYRO_LPM_1, GYRO_SUSPEND)
    elif mode == GYRO_DEEP_SUSPEND:
        bus.write_byte_data(BMI088_GYRO_ADDRESS, BMI088_GYRO_LPM_1, GYRO_DEEP_SUSPEND)

def setAccScaleRange(range):
    global _accRange
    if range == RANGE_3G:
        _accRange = 3.0
    elif range == RANGE_6G:
        _accRange = 6.0
    elif range == RANGE_12G:
        _accRange = 12.0
    elif range == RANGE_24G:
        _accRange = 24.0
    bus.write_byte_data(BMI088_ACC_ADDRESS, BMI088_ACC_RANGE, range)

def setAccOutputDataRate(odr):    
    data = bus.read_byte_data(BMI088_ACC_ADDRESS, BMI088_ACC_CONF);
    data = data & 0xf0;
    data = data | odr;
    
    bus.write_byte_data(BMI088_ACC_ADDRESS, BMI088_ACC_CONF, data)

def setGyroScaleRange(range):
    global _gyroRange
    if range == RANGE_2000:
        _gyroRange = 2000
    elif range == RANGE_1000:
        _gyroRange = 1000
    elif range == RANGE_500:
        _gyroRange = 500
    elif range == RANGE_250:
        _gyroRange = 250
    elif range == RANGE_125:
        _gyroRange = 125
    bus.write_byte_data(BMI088_GYRO_ADDRESS, BMI088_GYRO_RANGE, range)

def setGyroOutputDataRate(odr):
    bus.write_byte_data(BMI088_GYRO_ADDRESS, BMI088_GYRO_BAND_WIDTH, odr)
    
def getAccel():
    """Get accelerometer values (in multiples of g)        
    """
    if not _GYRO_INITED:
        init()
    accData=bus.read_i2c_block_data(BMI088_ACC_ADDRESS,BMI088_ACC_X_LSB,6)
    ax,ay,az=struct.unpack('hhh',struct.pack("BBBBBB",*accData))
    mult=_accRange / 32768
    return (ax*mult,ay*mult,az*mult)

def getGyro():
    """Get gyro values (in degrees per second)        
    """
    if not _GYRO_INITED:
        init()
    accData=bus.read_i2c_block_data(BMI088_GYRO_ADDRESS,BMI088_GYRO_RATE_X_LSB, 6)
    ax,ay,az=struct.unpack('hhh',struct.pack("BBBBBB",*accData))
    mult=_gyroRange / 32768
    return (ax*mult,ay*mult,az*mult)

#init()

if __name__=="__main__":
    while True:
        print((getAccel(),getGyro()))
        time.sleep(0.01)

