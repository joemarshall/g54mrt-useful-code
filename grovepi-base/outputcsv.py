import grovepi
import time

print("time,motion,sound")

while True:
  motion=grovepi.digitalRead(4)
  sound=grovepi.analogRead(4)
  # do some sensor processing here 
  print(time.time(),",",motion,",",sound)
  time.sleep(1)
