#!/usr/bin/python3
# -*- coding: ascii -*-
"""
    Writes and reads to the eeprom of the Grove NFC Tag module
    http://www.seeedstudio.com/wiki/Grove_-_NFC_Tag

    example usage:
        print (grovenfctag.readNFCData(0,16)) # display the first 16 bytes of the NFC tag
        
        time.sleep(0.1)# good idea to pause between read and writes
        grovenfctag.writeNFCData(0,[11,12,13,14,15,16,17,18,19])# write data to position 0
        
        print (grovenfctag.readNFCData(0,16)) # display the first 16 bytes of the NFC tag

"""

import time,sys

NFC_ADDR = 0x53

if sys.version_info >= (3, 0):    
    from quick2wire.i2c import I2CMaster, writing_bytes, reading,writing
    def readNFCData(addr,length):
      with I2CMaster() as master:    
        master.transaction(
            writing_bytes(NFC_ADDR, addr>>8,addr&0xff))
        read_results=master.transaction(reading(NFC_ADDR,length))
      return [c for c in read_results[0]]

    def writeNFCData(addr,data):
    #  print("actual write:"+str(data))
        for retries in range(10):
          try:
              with I2CMaster() as master:
                while len(data)>0:
                  master.transaction( writing(NFC_ADDR,[addr>>8,addr&0xff]+[c for c in data[0:4]]))
                  time.sleep(0.01)
                  data=data[4:]
                  addr+=4
              break
          except IOError as e:
            print(type(e),str(e)," retrying write")
        
else:      
    import smbus

    bus=smbus.SMBus(1)
        
    def readNFCData(addr,length):
        """ Read some data from eeprom of the Grove NFC Tag module 
        
            Args:
                addr:
                    Address to read data from
                
                length:
                    Number of bytes to read
                    
            Returns:
                Array of bytes
        """
        for retries in range(0,10):
            try:    
                bus.write_byte_data(NFC_ADDR,addr>>8,addr&0xff)
                result=[]
                for c in range(length):
                    result.append(bus.read_byte(NFC_ADDR))
                return result
            except IOError:
              time.sleep(0.1)
        print "Failed to read NFC data 10 times"

    def writeNFCData(addr,data):
        """ Write some data to the eeprom of the Grove NFC Tag module
        
            Args:
                addr:
                    address to write data to
                    
                data:
                    Array of bytes to write
        """
        for byte in data:
            for retries in range(0,10):
                try:    
                    bus.write_word_data(NFC_ADDR,addr>>8,(addr&0xff | (byte<<8)))
                    break
                except IOError:
                  time.sleep(0.01)
            time.sleep(0.01)
            addr+=1

      
class NFCTagBuffer:
    def __init__(self):
        self.writePosition=1
        self.bytes=[]
    
    # write data to the tag at current position and increment write position if needed
    def writeData(self, bytes):
        print("write:"+str(bytes))
        self.bytes.extend(bytes)
        self.flush(False)
        
    # if we have more than 4 bytes, actually write blocks out
    # if partialBuffer is true, then we write a partial buffer if we
    # have >1 and <4 bytes
    # buffer space 1 takes the current position
    def flush(self, partialBuffer=True):
        self.posAtStart=self.writePosition
        while len(self.bytes)>3:
            writeNFCData(self.writePosition*4,self.bytes[0:4])
            self.bytes=self.bytes[4:]
            self.writePosition+=1
            if self.writePosition>=2048:
                self.writePosition=1
        if partialBuffer and len(self.bytes)>0:
            self.bytes.extend([0]*(4-len(self.bytes)))
            writeNFCData(self.writePosition*4,self.bytes)
            self.bytes=[]
            self.writePosition+=1
            if self.writePosition>=2048:
                self.writePosition=1
        if self.posAtStart<self.writePosition:
            writeNFCData(0,[self.writePosition>>8,self.writePosition&0xff,0,0])

if __name__=="__main__":
    print (readNFCData(0,16))
    time.sleep(0.1)
    writeNFCData(0,[11,12,13,14,15,16,17,18,19])
    time.sleep(0.1)
    print( readNFCData(0,16))


