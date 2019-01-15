# this code is an example of a state machine implemented in python.
#
# How the state machine works:
# 
# we have a current state, in this case it is the currentState variable, and the change_state_counter
#
# Each time round the loop, you read the sensors
# and decide based on the current state, whether to change
# into a different state.
#
# This kind of thing is useful, because it avoids getting tangled up in complex if statements
# with sensing in different places, by always just sensing at the top of the loop, 
# and then dealing with it based on current state.
# 

import grovepi
import time

# here I define the states as named variables, because it makes the code below easier to read
# convention is that things in ALL_CAPITALS are constants, that are never changed

# example states - we are tracking a door which can be open or closed
STATE_UNKNOWN=0
STATE_DOOR_OPEN=1
STATE_DOOR_CLOSED=2

# definitions of what the sensors are connected to
ULTRASOUND_PIN = 5
ROTATION_SENSOR_PIN = 0

# some thresholds
THRESHOLD_DOOR_OPEN_ULTRASOUND=50
THRESHOLD_DOOR_OPEN_ROTATION=400

#variable which stores the current state
currentState=STATE_UNKNOWN

# we only change state when we've seen the sensors for a 5 seconds - this avoids fluctuating if there is noise
change_state_counter=0

# CSV header
print("ultrasound,rotation,currentState,change_state_counter")

while True:
    # first read the sensors
    ultrasound=grovepi.ultrasonicRead(ULTRASOUND_PIN)
    rotation=grovepi.analogRead(ROTATION_SENSOR_PIN)
    print("%d,%d,%d,%d"%(ultrasound,rotation,currentState,change_state_counter))
    
    # for each current state, check the sensors and decide whether to change state
    if currentState==STATE_UNKNOWN:
        # inital unknown state - guess from the current sensors
        if ultrasound > THRESHOLD_DOOR_OPEN_ULTRASOUND and rotation>THRESHOLD_DOOR_OPEN_ROTATION:
            # door is open
            currentState=STATE_DOOR_OPEN
        elif ultrasound< THRESHOLD_DOOR_OPEN_ULTRASOUND and rotation<THRESHOLD_DOOR_OPEN_ROTATION:
            # door is closed
            currentState=STATE_DOOR_CLOSED
        else:
            # the thresholds are each on the opposite directions, wait until the sensors die down before we decide on a state
            pass
    elif currentState==STATE_DOOR_OPEN:
        # we think the door is open - check if the sensors mean that it is closed
        # 
        if ultrasound< THRESHOLD_DOOR_OPEN_ULTRASOUND and rotation<THRESHOLD_DOOR_OPEN_ROTATION:
            # sensors say that the door is closed - add to the change state counter
            change_state_counter+=1
            if change_state_counter>5:
                # sensor has reported door closed for 5 seconds
                currentState=STATE_DOOR_CLOSED
                change_state_counter=0
        elif ultrasound > THRESHOLD_DOOR_OPEN_ULTRASOUND and rotation>THRESHOLD_DOOR_OPEN_ROTATION:
            # door definitely open - reset counter
            change_state_counter=0        
    elif currentState==STATE_DOOR_CLOSED:
        # we think the door is closed - check if the sensors mean that it is now open
        # 
        if ultrasound> THRESHOLD_DOOR_OPEN_ULTRASOUND and rotation>THRESHOLD_DOOR_OPEN_ROTATION:
            # both sensors say that the door is open - add to the change state counter
            change_state_counter+=1
            if change_state_counter>5:
                # sensor has reported door open for 5 seconds
                currentState=STATE_DOOR_OPEN
                change_state_counter=0
        elif ultrasound < THRESHOLD_DOOR_OPEN_ULTRASOUND and rotation<THRESHOLD_DOOR_OPEN_ROTATION:
            # door definitely closed - reset counter
            change_state_counter=0
    time.sleep(0.1)