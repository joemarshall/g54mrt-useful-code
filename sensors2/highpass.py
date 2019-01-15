import grovepi
import time
highPassed=0
constant=0.1
lastValue=0
print("Time,Raw data,High pass")
while True:
    value=grovepi.analogRead(2)
    # y(k) = a * (y(k-1)+ x(k)-x(k-1))
    highPassed=constant * (highPassed + value -lastValue)
    lastValue=value
    print("%4.4f,%4.4f,%4.4f"%(time.time(),value,highPassed))
    time.sleep(0.1)
