import grovepi
import grovelcd
import grove6axis
import grovenfctag
import time

print("timestamp,button,temperature,ultrasound")
while True:
    button=grovepi.digitalRead(2)
    temperature=grovepi.analogRead(0)
    ultrasound=grovepi.ultrasonicRead(7)
    print(time.time(),",",button,",",temperature,",",ultrasound)


