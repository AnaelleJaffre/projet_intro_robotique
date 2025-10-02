import numpy as np
import time
import pypot.dynamixel

from step_motors.goto2 import inv_kin

## DEBUG ##
DEBUG = 0 # 1 to enable debug_print 0 to deactivate
def debug_print(message):
    if DEBUG == 1:
        print(message)

## geometric parameters
Rwheels = 25.85 * 0.001; #wheel radius in m
Drob = 122 * 0.001; #space between both wheels in m

# control parameters 
adressMotorLeft = 1
adressMotorRight = 2

omegaMotorMove = 220 #angular speed in °/s (ie base moves 10 cm/s)
omegaMotorTurn = 202 #angular speed in °/s (ie base turns 90 °/s )

## position rob
XYTHETHA = [0,0,0] # movements along the Y axis 

def consigneAbsolute(Xc,Yc,Tc): #move at the coordinates from the Origin
    #compute vector for the base 
    Xc -= XYTHETHA[0]
    Yc -= XYTHETHA[1]
    Tc -= XYTHETHA[2]
    return(Xc,Yc,Tc)

def goTo(dxl_io, Xc,Yc,Tc):
    #convert to polar coordinates
    debug_print("compute GoTo L&T")
    Lgoto = np.sqrt(Xc*Xc+Yc*Yc) # Lgoto in m
    Tgoto = 180/np.pi*np.atan2(Yc,Xc) #Tgoto in deg
    debug_print(Lgoto)
    debug_print(Tgoto)
    #3 state movement 
    debug_print("============oriente base============")
    turn(dxl_io, Tgoto)
    debug_print("============move to============")
    move(dxl_io,Lgoto)
    debug_print("============final orientation============")
    turn(dxl_io, Tc-Tgoto)

def turn(dxl_io, Angle):
    #rotation of the wheels
    debug_print("compute consigne")
    consigne_motor = 1.025 * (1.0 * Drob)/(2.*Rwheels) * Angle # in °
    debug_print(consigne_motor)
    #set constant angular speed in opposition to turn the base
    debug_print("set speed")
    dxl_io.set_moving_speed({adressMotorLeft: omegaMotorTurn}) 
    dxl_io.set_moving_speed({adressMotorRight: omegaMotorTurn})
    #time = angle/angular_speed
    debug_print("do for :")
    debug_print(consigne_motor/omegaMotorTurn)
    time.sleep(abs(consigne_motor/omegaMotorTurn))
    #stops the motors
    debug_print("motor stop")
    dxl_io.set_moving_speed({adressMotorLeft: 0}) 
    dxl_io.set_moving_speed({adressMotorRight: 0})

def turn_line(dxl_io, dx, V0, K_cor):
    """
    Proportional controller changing rotational speed based on dy component of error to target
    :param dxl_io : DXL motor
    :param dy : y error to target
    :param V0 : constant linear speed
    :param K_cor : Proportional term
    """
    omega = K_cor * dx
    [SL, SR] = inv_kin(V0, omega)
    dxl_io.set_moving_speed({adressMotorLeft: SL})
    dxl_io.set_moving_speed({adressMotorRight: -SR})

def move(dxl_io, Length):
    #rotation of the wheels
    debug_print("compute consigne")
    consigne_motor = 180/np.pi * Length / Rwheels # in °
    debug_print(consigne_motor)
    #set constant angular speed to move the base
    debug_print("set speed")
    dxl_io.set_moving_speed({adressMotorLeft: omegaMotorMove}) 
    dxl_io.set_moving_speed({adressMotorRight: -omegaMotorMove})
    #time = lenght/linear_speed
    debug_print("do for :")
    debug_print(consigne_motor/omegaMotorMove)
    time.sleep(abs(consigne_motor/omegaMotorMove))
    #stops the motors
    debug_print("motor stop")
    dxl_io.set_moving_speed({adressMotorLeft: 0}) 
    dxl_io.set_moving_speed({adressMotorRight: 0})
