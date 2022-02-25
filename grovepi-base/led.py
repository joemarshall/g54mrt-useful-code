import grovepi

def on(pin):
    grovepi.pinMode(pin,"OUTPUT")
    grovepi.digitalWrite(pin,1)
    
def off(pin):
    grovepi.pinMode(pin,"OUTPUT")
    grovepi.digitalWrite(pin,0)
