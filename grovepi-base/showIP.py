#!/usr/bin/python3

import grovelcd
import time
import subprocess
import re
import socket
import grovepi
import os.path

badFirmware=True
try:
    version = grovepi.version()
    version=version.replace(".","")
    badFirmware=False
except:
    version="???"
try:
    burnDate=time.strftime("%d%m",time.gmtime(os.path.getmtime('/boot/burning-date.txt')))
except:
    burnDate="0000"
imgDate=""
try:
    with open('/boot/image-date.txt') as im:
      imgDate=im.read()
except IOError:
    imgDate=""

gitVer=subprocess.check_output("git --git-dir=/home/pi/g54mrt-useful-code/.git log -1 --format=\"%at\"  | xargs -I{} date -d @{} +%d%m%y",shell=True) 
gitVer=gitVer.decode()    
print(gitVer)
grovelcd.setText("MRT%s %s\nIMG FW%s (%s)"%(imgDate[0:4]+imgDate[6:8],gitVer[0:6],version,burnDate))

grovelcd.setRGB(128,128,128)
cyclePos=1
#grovelcd.setText("No address yet")

curText=""

time.sleep(5)

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

countLeft=300
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
        countLeft=30
      if values[0]=='default':
        pass
#        grovelcd.setText("%s\ngateway"%values[2])
      else:
        if values[2].find("eth")!=-1:
          ethAddr=formatAddr(values[8],"e")
        if values[2].find("wlan")!=-1:
          wlanAddr=formatAddr(values[8],"w")      
  adapterList=subprocess.check_output(['ifconfig'])
  if adapterList.find(b"wlan0")==-1:
      wlanAddr="Plug USB WIFI in"        
  newText=ethAddr+"\n"+wlanAddr
  if newText!=curText:
     curText=newText
     grovelcd.setText(newText)
  time.sleep(2.0)
  if countLeft!=None:
    countLeft-=2
  
