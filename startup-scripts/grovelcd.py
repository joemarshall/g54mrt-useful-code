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

def setText(text,clear=False):
  """ Set text on display to <text> """
  global firstTime
  if clear or firstTime:
    textCommand(0x01) # clear display
    time.sleep(0.1)
    textCommand(0x08|0x04) # display on, no cursor
    time.sleep(0.1)
    textCommand(0x20|0x08) # two line
    firstTime=False
  else:
    textCommand(0x80) # go to start
  count = 0
  row=0
  
  line1=""
  line2=""
  for c in text:
    if c=="\n":
      row=1
      count=0
    elif row==0:
      line1+=c
    elif row==1:
      line2+=c
    count+=1
    if count>=16:
      row=1
  for c in range(16):
    if c<len(line1):
      bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(line1[c]))
    else:
      bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(' '))
  textCommand(0xc0)
  for c in range(16):
    if c<len(line2):
      bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(line2[c]))
    else:
      bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(' '))
    

if __name__=="__main__":
    setText("Hello world, \nHow are you")
    setRGB(0,128,64)
    for c in range(0,255):
      setRGB(c,255-c,0)
      time.sleep(0.01)
    setRGB(0,255,0)
    setText("Bye bye")



