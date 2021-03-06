import grovepi
import time
import collections # for deque class

# the following code does the median filter itself
    
# create a deque for history
# a deque is a double ended list,
# put things in the end when it is full
# (when it contains maxlen values), and things 
# will be pushed off the other end     
historyBuffer=collections.deque(maxlen=21)

print("Time,Raw data,Median")

while True:
  dataPoint=grovepi.analogRead(0)
  historyBuffer.append(dataPoint)
  orderedHistory=sorted(historyBuffer)
  median=orderedHistory[int(len(orderedHistory)/2)]
  print("%4.4f,%4.4f,%4.4f"%(time.time(),dataPoint,median))
  time.sleep(0.1)