import grovepi
import time

sneak_detect=0
print "timestamp,motion,sound,sneak_detect"
while True:
  m=grovepi.digitalRead(4)
  s=grovepi.analogRead(0)
  # a loud noise is a sneak
  if s>200:
    sneak_detect=1
  # or a medium noise and motion sensor firing
  elif s>100 and m==1:
    sneak_detect=1
  else:
  # maybe don't fire if we hear no big noises 
  # to avoid false positives
    sneak_detect=0
  
  print "%f,%d,%d,%d"%(time.time(),m,s,sneak_detect)
  time.sleep(.1)
