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

#compute raw angle of each motors based on measured speed of the motors and the sampling frequency
def call_motor_angle(f_ech,dxl_io):
    rawDataLeft = dxl_io.read_speed({adressMotorLeft})*f_ech
    rawDataRight = dxl_io.read_speed({adressMotorRight})*f_ech
    return(rawDataLeft, rawDataRight)

#compute distance and angle change based on wheels variations
def vect_update(f_ech,dxl_io):
    deltaLeft, deltaRight = call_motor_angle(f_ech,dxl_io)

    #direct kinematics
    L = Rwheels/2 * (deltaRight-deltaLeft)
    Tetha = Rwheels/Drob * (deltaRight-deltaLeft)

    return (L, Tetha)

#add change vector to previous position to get the base position in world frame
def update_odom(f_ech,dxl_io):

    l,t = vect_update(f_ech,dxl_io)

    XYTHETHA[2] += t
    #projection from robot frame to world frame
    X = XYTHETHA[0] + l*np.cos(XYTHETHA[2])
    Y = XYTHETHA[1] + l*np.sin(XYTHETHA[2])

    XYTHETHA[0] += X
    XYTHETHA[1] += Y

#function to be called by the rest of the code to get the current estimated position of the base
def get_odom(f_ech,dxl_io):
    update_odom(f_ech,dxl_io)
    return(XYTHETHA)


