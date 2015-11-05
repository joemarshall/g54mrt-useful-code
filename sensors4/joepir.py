import grovepi
import time

PIR1_PIN = 2
PIR2_PIN = 3

lastPIR1=None
lastPIR2=None

lastNumberIn=0
numberIn=0
startTime=time.time()
print "time,pir1,pir2,numberIn"

while True:
    pir1=grovepi.digitalRead(PIR1_PIN)
    pir2=grovepi.digitalRead(PIR2_PIN)
    curTime=time.time()
    
    # is the incoming PIR firing?
    if pir1:
        # ignore multiple firings of the PIR within two seconds
        if lastPIR1==None or curTime-lastPIR1>2:
            lastPIR1=curTime
            # did we recently see PIR 2? (within the last 2 seconds)
            # if so, lets assume someone came out, otherwise we assume it is someone coming in and do nothing until we see PIR2
            if lastPIR2!=None and lastPIR1-lastPIR2<2:
                numberIn-=1
    # is the outgoing PIR firing
    if pir2:
        # ignore multiple firings of the PIR within two seconds
        if lastPIR2==None or curTime-lastPIR2>2:
            lastPIR2=curTime
            # did we recently see PIR 2? (within the last 2 seconds)
            # if so, lets assume someone came out, otherwise we assume it is someone coming in and do nothing until we see PIR2
            if lastPIR1!=None and lastPIR2-lastPIR1<2:
                numberIn+=1
    print "%f,%d,%d,%d"%(curTime-startTime,pir1,pir2,numberIn)
    time.sleep(0.5)