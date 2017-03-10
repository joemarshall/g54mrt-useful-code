import grovepi
import time
lowPass=0
highPass=0
constantHP=0.5
constantLP=0.1
lastValue=0
while True:
    value=grovepi.analogRead(0)
    # y(k) = a * (y(k-1)+ x(k)-x(k-1))
    highPass=constantHP * (highPass + value -lastValue)
    lastValue=value
    
    lowPass=lowPass*(1.0-constantLP) + highPass * constantLP
    print "High, band pass: % 4.4f % 4.4f"%(highPass,lowPass)
    time.sleep(0.1)
