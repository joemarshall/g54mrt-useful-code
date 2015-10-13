import random
import collections

# generate a rising line with some random noise added to test this with
testData=[]
for c in range(0,1000):
    # normal / gauss random noise, variance 50 (so very noisy)
    noiseValue=random.gauss(0,50)
    dataValue=c
    testData.append(dataValue+noiseValue)

# the following code does the median filter itself
    
# create a deque for history
# a deque is a double ended list,
# put things in the end when it is full
# (when it contains maxlen values), and things 
# will be pushed off the other end     
historyBuffer=collections.deque(maxlen=21)
for dataPoint in testData:
    historyBuffer.append(dataPoint)
    orderedHistory=sorted(historyBuffer)
    median=orderedHistory[int(len(orderedHistory)/2)]
    print dataPoint,",",median
