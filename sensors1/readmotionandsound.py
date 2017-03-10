import grovepi
import time
print "timestamp,motion,sound"
while True:
  m=grovepi.digitalRead(4)
  s=grovepi.analogRead(0)
  print "%f,%d,%d"%(time.time(),m,s)
  time.sleep(1)
