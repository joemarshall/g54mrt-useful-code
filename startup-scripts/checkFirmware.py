import sys
import grovepi
import grovelcd
import time
import os
from subprocess import call


def doUpdate():
    retVal=call(["/usr/bin/avrdude","-c","gpio","-p","m328p"])
    if retVal!=0:
    # needs jumper between ISP and reset
        grovelcd.setText("Jumper wire fromD4 to ISP reset")
        while grovepi.digitalRead(2)==0:
            time.sleep(0.01)
        while grovepi.digitalRead(2)==1:
            time.sleep(0.01)
    firmwarePath=os.path.join(os.path.dirname(os.path.realpath(__file__)),"grove_pi_firmware.hex")
    print firmwarePath
    grovelcd.setText("Try update firmware\n---------------")
    retVal1=call(["/usr/bin/avrdude","-c","gpio","-p","m328p","-U","lfuse:w:0xFF:m"])
    if retVal1==0:
        grovelcd.setText("Try update firmware\n**----------")
        retVal2=call(["/usr/bin/avrdude","-c","gpio","-p","m328p","-U","hfuse:w:0xDA:m"])
        grovelcd.setText("Try update firmware\n****--------")
        retVal3=call(["/usr/bin/avrdude","-c","gpio","-p","m328p","-U","efuse:w:0x05:m"])
        grovelcd.setText("Try update firmware\n******------")
        retVal4=call(["/usr/bin/avrdude","-c","gpio","-p","m328p","-U","flash:w:%s"%(firmwarePath)])
        if retVal4==0:
            newVer=grovepi.version()
            grovelcd.setText("Update ok\n"+newVer)
        else:
           grovelcd.setText("Update failed\nPress button")
    else:
       grovelcd.setText("Update failed\nPress button")
    while grovepi.digitalRead(2)==0:
        time.sleep(0.01)
    while grovepi.digitalRead(2)==1:
        time.sleep(0.01)
    grovelcd.setText("")


needsUpdate=False
currentVersion= grovepi.version().split(".")
verNum=map(int,currentVersion)
if verNum<(1,2,7) or verNum[0]==255:
    needsUpdate=True

if needsUpdate:
    grovelcd.setRGB(128,128,128)
    grovelcd.setText("Needs firmware\npress D2 button")

    while grovepi.digitalRead(2)==0:
        time.sleep(0.01)
    ## require release of button
    while grovepi.digitalRead(2)==1:
        time.sleep(0.01)
    
    doUpdate()


