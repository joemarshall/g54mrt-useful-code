import sys
import grovepi
import grovelcd
import time
import os
from subprocess import call


def doUpdate():
    retVal=call(["/usr/bin/avrdude","-c","linuxgpio","-p","m328p"])
    if retVal!=0:
    # needs jumper between ISP and reset
        grovelcd.setText("Jumper wire fromD4 to ISP reset")
        while grovepi.digitalRead(2)==0:
            time.sleep(0.01)
        while grovepi.digitalRead(2)==1:
            time.sleep(0.01)
    firmwarePath=os.path.join(os.path.dirname(os.path.realpath(__file__)),"grove_pi_firmware.hex")
    print (firmwarePath)
    grovelcd.setText("Try update firmware\n---------------")
    retVal=call(["/usr/bin/avrdude","-c","linuxgpio","-p","m328p","-U","lfuse:w:0xFF:m"])
    if retVal==0:
        grovelcd.setText("Try update\n**----------")
        retVal=call(["/usr/bin/avrdude","-c","linuxgpio","-p","m328p","-U","hfuse:w:0xDA:m"])
    if retVal==0:
        grovelcd.setText("Try update\n****--------")
        retVal=call(["/usr/bin/avrdude","-c","linuxgpio","-p","m328p","-U","efuse:w:0xFD:m"])
    if retVal==0:
        grovelcd.setText("Try update\n******------")
        retVal=call(["/usr/bin/avrdude","-c","linuxgpio","-p","m328p","-U","flash:w:%s"%(firmwarePath)])
    if retVal==0:
        time.sleep(0.5)
        newVer=grovepi.version()
        grovelcd.setText("Update ok\n"+newVer)
        time.sleep(5)
        import showIP
    else:
       grovelcd.setText("Update failed\nPress button")
    grovelcd.setText("")

#time.sleep(5)
needsUpdate=False
try:
    currentVersion= grovepi.version().split(".")
    verNum=map(int,currentVersion)
    if verNum!=[1,4,0] or verNum[0]==255:
        needsUpdate=True
except:
    needsUpdate=True

if needsUpdate:
    grovelcd.setRGB(128,128,128)
    grovelcd.setText("Old firmware")

   # while grovepi.digitalRead(2)==0:
  #      time.sleep(0.01)
    ## require release of button
  #  while grovepi.digitalRead(2)==1:
  #      time.sleep(0.01)
    
    doUpdate()


