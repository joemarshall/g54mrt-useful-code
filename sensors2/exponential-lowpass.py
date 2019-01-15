import grovepi
import time

lowPassed=0
constant=0.1
print("Time,Raw data, Low pass")
while True:
    value=grovepi.analogRead(0)
    lowPassed=lowPassed*(1.0-constant) + value * constant
    print("%4.4f,%4.4f,%4.4f"%(time.time(),value,lowPassed))
    time.sleep(0.05);
