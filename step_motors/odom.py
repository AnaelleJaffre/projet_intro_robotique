import numpy as np
import pypot.dynamixel



## DEBUG ##
DEBUG = 0 # 1 to enable debug_print 0 to deactivate
def debug_print(*args):
    if DEBUG:
        print(*args)


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
    #debug_print(dxl_io.get_present_speed({adressMotorLeft})[0])
    rawDataLeft = dxl_io.get_present_speed({adressMotorLeft})[0] / f_ech
    rawDataRight = - dxl_io.get_present_speed({adressMotorRight})[0] /  f_ech
    # debug_print("motor angle")
    # debug_print(rawDataLeft)
    # debug_print(rawDataRight)
    return(rawDataLeft, rawDataRight)

#compute distance and angle change based on wheels variations
def vect_update(f_ech,dxl_io):
    deltaLeft, deltaRight = call_motor_angle(f_ech,dxl_io)
    
    #direct kinematics
    L = Rwheels/2 * (np.deg2rad(deltaRight) + np.deg2rad(deltaLeft))
    Tetha = Rwheels/Drob * (deltaRight - deltaLeft)
    #debug_print("vect")
    # debug_print(L)
    # debug_print(Tetha)
    return (L, Tetha)

#add change vector to previous position to get the base position in world frame
def update_odom(f_ech,dxl_io):

    l,t = vect_update(f_ech,dxl_io) # in m, in deg

    XYTHETHA[2] += t
    #projection from robot frame to world frame
    dX = -l*np.sin(XYTHETHA[2])
    dY = l*np.cos(XYTHETHA[2])
    debug_print("dX :", dX)
    debug_print("dY :", dY)
    XYTHETHA[0] += dX
    XYTHETHA[1] += dY

#function to be called by the rest of the code to get the current estimated position of the base
def get_odom(f_ech,dxl_io):
    update_odom(f_ech,dxl_io)
    return(XYTHETHA)


