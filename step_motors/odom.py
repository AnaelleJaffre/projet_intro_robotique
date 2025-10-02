import numpy as np
import pypot.dynamixel

## geometric parameters
Rwheels = 25.85*0.001; #wheel radius in m
Drob = 117.2*0.001; #space between both wheels in m

# control parameters 
adressMotorLeft = 1
adressMotorRight = 2

## position
XYTHETHA = [0,0,0] # movements along the Y axis 


def vect_update(f_ech,dxl_io):
    deltaLeft, deltaRight = call_motor_angle(f_ech,dxl_io)

    #kinematics
    L = Rwheels/2 * (deltaRight-deltaLeft)
    Tetha = Rwheels/Drob * (deltaRight-deltaLeft)

    return (L, Tetha)

def update_odom(f_ech,dxl_io):

    l,t = vect_update(f_ech,dxl_io)

    XYTHETHA[2] += t
    X = XYTHETHA[0] + l*np.cos(XYTHETHA[2])
    Y = XYTHETHA[1] + l*np.sin(XYTHETHA[2])

    XYTHETHA[0] += X
    XYTHETHA[1] += Y

def get_odom(f_ech,dxl_io):
    update_odom(f_ech,dxl_io)
    return(XYTHETHA)

def call_motor_angle(f_ech,dxl_io):
    rawDataLeft = dxl_io.read_speed({adressMotorLeft})*f_ech
    rawDataRight = dxl_io.read_speed({adressMotorRight})*f_ech
    return(rawDataLeft, rawDataRight)

