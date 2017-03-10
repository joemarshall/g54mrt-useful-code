import grovepi
import time

PIR1_PIN = 4
PIR2_PIN = 3

lastPIR1Time=None
lastPIR2Time=None

lastNumberIn=0
numberIn=0
startTime=time.time()
print "time,pir1,pir2,numberIn"

# we only do things when the PIR values *rise*
lastPIR1=0
lastPIR2=0

while True:
    pir1=grovepi.digitalRead(PIR1_PIN)
    pir2=grovepi.digitalRead(PIR2_PIN)
    
    curTime=time.time()
    
    # is the incoming PIR value rising?
    if pir1 and lastPIR1==0:
        lastPIR1Time=curTime
        # did we recently see PIR 2? (within the last 2 seconds)
        # if so, lets assume someone came out, otherwise we assume it is someone coming in and 
        # do nothing until we see PIR2
        if lastPIR2Time!=None and curTime-lastPIR2Time<2:
            numberIn-=1
    # is the outgoing PIR rising?
    if pir2 and lastPIR2==0:
        lastPIR2Time=curTime
        # did we recently see PIR 1? (within the last 2 seconds)
        # if so, lets assume someone came out, otherwise we assume it is someone coming in and 
        # do nothing until we see PIR1
        if lastPIR1Time!=None and curTime-lastPIR1Time<2:
            numberIn+=1
    lastPIR1=pir1
    lastPIR2=pir2    
    print "%f,%d,%d,%d"%(curTime-startTime,pir1,pir2,numberIn)
    time.sleep(0.5)