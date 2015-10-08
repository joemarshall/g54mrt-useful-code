from matplotlib.pyplot import *
from matplotlib.ticker import FuncFormatter
import time,calendar
import csv

xValues=[]
yValues=[]

# in this bit, we read the CSV file into python
with open("sensordata-1443654000000-1443826800000.csv") as file:
  reader=csv.DictReader(file)
  for line in reader:
    xValues.append(float(line["timestamp"]))
    yValues.append(int(line["light"]))

#plot the CSV file on the graph    
plot(xValues,yValues)
startTime=xValues[0]
endTime=xValues[-1]

print startTime,endTime,len(yValues),min(yValues),max(yValues)

# this bit of code puts nice labels on the chart for each hour
tickPos=[]
tickLabel=[]
for c in range(0,int((endTime-startTime)/3600)):
    tickTime=startTime+c*3600
    tickPos.append(tickTime)
    tickLabel.append(time.strftime('%H:%M',time.gmtime(tickTime)))  
xticks(tickPos,tickLabel,rotation=90)

xlim(startTime,endTime) # set x axis to fill our time range
ylim(0,1024)# set the y axis to the full sensor axis
show()
    