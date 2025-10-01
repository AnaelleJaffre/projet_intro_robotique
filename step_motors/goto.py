import numpy as np
import time
import pypot.dynamixel

## geometric parameters
Rwheels = 25.85*0.001; #wheel radius in m
Drob = 117.2*0.001; #space between both wheels in m

## position rob
XYTHETHA = [0,0,0] # movements along the Y axis 

def consigneAbsolute(Xc,Yc,Tc): #move at the coordinates from the Origin
    #compute vector for the base 
    Xc -= XYTHETHA[0]
    Yc -= XYTHETHA[1]
    Tc -= XYTHETHA[2]
    return(Xc,Yc,Tc)

def goTo(Xc,Yc,Tc):
    #convert to polar coordinates
    Lgoto = np.sqrt(Xc*Xc+Yc*Yc)
    Tgoto = np.arctan(Yc/Xc)
    #3 state movement 
    turn(Tgoto)
    move(Lgoto)
    turn(Tc-Tgoto)

def turn(Angle):
    #rotation of the wheels
    consigne_motor = Drob/Rwheels * Angle
    #set constant angular speed in opposition to turn the base
    dxl_io.set_moving_speed({1: omegaMotor}) 
    dxl_io.set_moving_speed({2: -omegaMotor})
    #time = angle/angular_speed
    time.sleep(consigne_motor/omegaMotor)
    #stops the motors
    dxl_io.set_moving_speed({1: 0}) 
    dxl_io.set_moving_speed({2: 0})

def move(Lenght):
    #rotation of the wheels
    consigne_motor = 2/Rwheels * Lenght
    #set constant angular speed to move the base
    dxl_io.set_moving_speed({1: omegaMotor}) 
    dxl_io.set_moving_speed({2: omegaMotor})
    #time = lenght/linear_speed
    time.sleep(consigne_motor/omegaMotor)
    #stops the motors
    dxl_io.set_moving_speed({1: 0}) 
    dxl_io.set_moving_speed({2: 0})
