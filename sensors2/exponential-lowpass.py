import grovepi

filtOut=0
constant=0.1
while True:
    value=grovepi.analogRead(0)
    filtOut=filtOut*(1.0-constant) + value * constant
    print "Smoothed:",filtOut
