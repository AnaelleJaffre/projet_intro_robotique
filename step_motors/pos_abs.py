import numpy as np

## geometric parameters
Rwheels = 25.85*0.001; #wheel radius in m
Drob = 117.2*0.001; #space between both wheels in m

## position
XYTHETHA = [0,0,0] # movements along the Y axis 

rawData = [0,0] # left then right

def vect_update():
    rawDataLeft, rawDataRight = call_motor_angle()
    # change between calls
    deltaLeft = rawDataLeft-rawData[0]
    deltaRight = rawDataRight-rawData[1]
    #kinematics
    L = Rwheels/2 * (deltaRight-deltaLeft)
    Tetha = Rwheels/Drob * (deltaRight-deltaLeft)
    #update motor angle for next call
    rawData[0] = rawDataLeft
    rawData[1] = rawDataRight

    return (L, Tetha)

def update_odom():

    l,t = vect_update()

    XYTHETHA[2] += t
    X = XYTHETHA[0] + l*np.cos(XYTHETHA[2])
    Y = XYTHETHA[1] + l*np.sin(XYTHETHA[2])

    XYTHETHA[0] += X
    XYTHETHA[1] += Y

def get_odom():
    return(XYTHETHA)

def call_motor_angle():
    return(rawDataLeft, rawDataRight)

