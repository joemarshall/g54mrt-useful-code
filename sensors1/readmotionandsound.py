import grovepi
import time
print "timestamp,motion,sound"
while True:
  m=grovepi.digitalRead(4)
  s=grovepi.analogRead(0)
  print time.time(),",",m,",",s
  time.sleep(1)
