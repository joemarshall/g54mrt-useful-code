#!/usr/bin/python3
# -*- coding: ascii -*-
"""
    Writes text to the Grove RGB LCD, and controls the backlight colour

    example code:
        # set text (\\n goes onto the second line 
        grovelcd.setText("Hello world, \\nHow are you") 
        # set the backlight:
        # red off
        # green half of full brightness
        # blue one quarter of full brighness.
        grovelcd.setRGB(0,128,64)
"""

import time,sys

DISPLAY_RGB_ADDR=0x62
DISPLAY_TEXT_ADDR=0x3e

import smbus2 as smbus
import math
from collections import deque
firstTime=True

bus=smbus.SMBus(1)

def setRGB(r,g,b):
    """
        Set backlight colour to (r,g,b)
        
        Args:
            r:
                red (0=off, 255 = fully on)
            g:
                green (0=off, 255 = fully on)
            b:
                blue (0=off, 255 = fully on)
    """
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

def textCommand(cmd):
    """Used internally, don't mess with it unless you know what you're doing"""
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)


def setCustomChar(charNum,charData):
    charNum&=0x07
    cmd=0x40|(charNum<<3)
    textCommand(cmd)
    bus.write_i2c_block_data(DISPLAY_TEXT_ADDR,0x40,charData)

def makeGraphChars():
    for c in range(8):
        graphData= [0xf if d==c else 0 for d in range(8)]
#        graphData= [0x4 for d in range(7)]
        setCustomChar(c,graphData)        


_prevData=[[ord(' ')]*16,[ord(' ')]*16]        

def setText(text,clear=False):
  """ Set text on display to <text> """
  global firstTime,_prevData
  if clear or firstTime:
    textCommand(0x01) # clear display
    time.sleep(0.1)
    textCommand(0x08|0x04) # display on, no cursor
    time.sleep(0.1)
    textCommand(0x20|0x08) # two line
    time.sleep(0.1)
    textCommand(0x04|0x02) # left to right text
    time.sleep(0.1)
    
    firstTime=False
  count = 0
  row=0
  
  line1=[]
  line2=[]
  for c in text:
    if c=="\n":
      row=1
      count=0
    elif row==0:
      line1+=[ord(c)]
    elif row==1:
      line2+=[ord(c)]
    count+=1
    if count>=16:
      row=1
  textData1=line1+(16-len(line1))*[ord(' ')]
  textData2=line2+(16-len(line2))*[ord(' ')]
  thisData=[textData1,textData2]
  if thisData!=_prevData:
      _prevData=thisData
      textCommand(0x80) # line 1 select
      bus.write_i2c_block_data(DISPLAY_TEXT_ADDR,0x40,textData1)
      textCommand(0xc0) # line 2 select
      bus.write_i2c_block_data(DISPLAY_TEXT_ADDR,0x40,textData2)

    
def addGraphData(data,x,y,columns,rows):
    data=list(data)
    global _prevData
    numChars=16//columns
    startChar=0
    if columns>1 and x==1:
        startChar=8
    if rows==2:
        rowIDX=1 if y==1 else 0
        thisRow=_prevData[rowIDX][:]
        for c in range(0,numChars):
            dataStart=(c*len(data))//numChars
            dataEnd=((c+1)*len(data))//numChars
            if dataEnd<=dataStart:
                dataEnd=dataStart+1
            outVal=max(data[dataStart:dataEnd])
            outVal=max(outVal,0)
            outVal=min(outVal,1)
            outVal=7-math.floor(outVal*7.5)
            thisRow[c+startChar]=outVal
        if _prevData[rowIDX]!=thisRow:
            _prevData[rowIDX]=thisRow
            textCommand(0x80|(0x40*rowIDX)) # line X select
            bus.write_i2c_block_data(DISPLAY_TEXT_ADDR,0x40,thisRow)            
    else:
        row1,row2=_prevData[0][:],_prevData[1][:]
        for c in range(0,numChars):
            dataStart=(c*len(data))//numChars
            dataEnd=((c+1)*len(data))//numChars
            if dataEnd<=dataStart:
                dataEnd=dataStart+1
            outVal=max(data[dataStart:dataEnd])
            outVal=max(outVal,0)
            outVal=min(outVal,1)
            outVal=15-math.floor(outVal*15.5)
            if outVal>=8:
                row2[c+startChar]=outVal-8
                row1[c+startChar]=ord(' ')
            else:
                row1[c+startChar]=outVal
                row2[c+startChar]=ord(' ')
        if _prevData[0]!=row1:
            _prevData[0]=row1
            textCommand(0x80) # line X select
            bus.write_i2c_block_data(DISPLAY_TEXT_ADDR,0x40,row1)            
        if _prevData[1]!=row2:
            _prevData[0]=row2
            textCommand(0xc0) # line X select
            bus.write_i2c_block_data(DISPLAY_TEXT_ADDR,0x40,row2)            
        _prevData=[row1,row2]
        # spread graph over 2 rows
        
        

if __name__=="__main__":
    setRGB(0,128,64)
    setText("")
    makeGraphChars()
    setText("YO, \n"+"".join([chr(0),chr(1),chr(2),chr(3),chr(4),chr(5),chr(6),chr(7)]))
    x=0
    graphData=[]
    for c in range(50):
        graphData.append(0.5+0.5*math.sin(x))
        x+=0.1
    for c in range(0,255):
      setRGB(c,255-c,0)
      graphData.append(0.5+0.5*math.sin(x))
      graphData=graphData[1:]
      x+=0.1
      addGraphData(graphData,1,0,2,1)
      time.sleep(0.01)
    setRGB(0,255,0)
#    setText("Bye bye")



