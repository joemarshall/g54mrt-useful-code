import grovepi

filtOut=0
constant=0.1
lastValue=0
while True:
    value=grovepi.analogRead(0)
    # y(k) = a * (y(k-1)+ x(k)-x(k-1))
    filtOut=constant * (filtOut + value -lastValue)
    lastValue=value
    print "High passed:",filtOut
