import grovepi
import time
print("timestamp,motion,sound,button")
while True:
  m=grovepi.digitalRead(4)
  s=grovepi.analogRead(0)
  b=grovepi.digitalRead(5)
  print("%f,%d,%d,%d"%(time.time(),m,s,b))
  time.sleep(.1)
