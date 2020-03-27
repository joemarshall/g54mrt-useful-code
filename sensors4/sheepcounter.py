import grovepi
import time


TIMES_FIRED_TO_COUNT=4 # Threshold for if we detect a sheep passing

curFired=0
lastOn=False
sheepCount=0

print("time,ultrasonic,sheepCount")
while True:
  dist=grovepi.ultrasonicRead(7)#
  on = lastOn
  if dist>100:
    if curFired>0:  
        curFired-=1
    else:
      on=False
  else:
    curFired+=1
    if curFired==TIMES_FIRED_TO_COUNT:
      on=True
  if on and not lastOn:
    sheepCount+=1
  lastOn=on
  print("%f,%d,%d"%(time.time(),dist,sheepCount))
    
    