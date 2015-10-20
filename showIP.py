#!/usr/bin/python3

import grovelcd
import time
import subprocess
import re
import socket

grovelcd.setRGB(128,128,128)
cyclePos=1
grovelcd.setText("No address yet")

# changed to only say IP address, so as not to confuse people with gateway addresses

def formatAddr(addr,type):
  retVal=addr
  if len(retVal)<14:
    retVal+=" "*(14-len(retVal))
  if len(retVal)==14:
    retVal+=":"
  if len(retVal)<16:
    retVal+=type
  return retVal[0:16]

countLeft=60
while countLeft==None or countLeft>0:
#  if startTime!=None:
#    print startTime,time.time(),startTime,startTime+10,time.time()<startTime+30
  result=subprocess.check_output(['ip','route'])
  result=result.decode()
  curPos=0
  ethAddr="No ethernet"
  wlanAddr="No wireless"
  for line in result.split('\n'):
    values=re.split('\s+',line) 
    if len(values)>2:
      if countLeft==None:
        countLeft=10
      if values[0]=='default':
        pass
#        grovelcd.setText("%s\ngateway"%values[2])
      else:
        if values[2].find("eth")!=-1:
          ethAddr=formatAddr(values[8],"e")
        if values[2].find("wlan")!=-1:
          wlanAddr=formatAddr(values[8],"w")
    grovelcd.setText(ethAddr+"\n"+wlanAddr)
  time.sleep(2.0)
  if countLeft!=None:
    countLeft-=2
  
