import numpy as np
import time
import pypot.dynamixel
import step_motors.odom as odom

## DEBUG ##
DEBUG = 0 # 1 to enable print 0 to deactivate
def debug_print(message):
    if DEBUG:
        print(message)

## geometric parameters
Rwheels = 25.85*0.001; #wheel radius in m
Drob = 117.2*0.001; #space between both wheels in m

# control parameters 
adressMotorLeft = 1
adressMotorRight = 2

omegaMotorMove = 220 #angular speed in °/s (ie base moves 10 cm/s)
omegaMotorTurn = 202 #angular speed in °/s (ie base turns 90 °/s )
satisfactory_area = 0.01 #circle around target in m

## corr parameters
K_lin =0.1 #Hz
K_ang =0.1 #Hz

lin_speed = 0
ang_speed = 0
last_ang_speed = 0


def inv_kin(V,O):
    speedLeft = 180/np.pi*V/Rwheels + Drob/(2*Rwheels)*O
    speedRight = 180/np.pi*V/Rwheels - Drob/(2*Rwheels)*O
    return([speedLeft,speedRight])

def turn_line(dxl_io, dY, K_cor, V0):
    Omega = K_cor * dY #the more the gap the more the angular correction
    Vlin = V0#the more the gap the slower we go
    SL, SR = inv_kin(Vlin, Omega)
    dxl_io.set_moving_speed({adressMotorLeft: SL}) 
    dxl_io.set_moving_speed({adressMotorRight: -SR})  
    print("Omega : ",Omega)  



def update_error_vector(current_pos: tuple[float,float], target_pos: tuple[float,float]): #error vector
    eps_L = target_pos[0]-current_pos[0]
    eps_T = target_pos[1]-current_pos[1]
    return([eps_L,eps_T])

def get_current_pos(): 
    X,Y,T = odom.get_odom()
    L = np.sqrt(X*X+Y*Y)
    return([L,T])

def set_speed(dxl_io,command: tuple[float,float]): 
    dxl_io.set_moving_speed({adressMotorLeft: command[0]}) 
    dxl_io.set_moving_speed({adressMotorRight: -command[1]})

def set_command(error_vector_pos: tuple[float,float],final_angle,dxl_io):
    lin_speed += K_lin * error_vector_pos[0]
    ang_speed += K_ang * error_vector_pos[1]
    if (error_vector_pos[0] > satisfactory_area):
        debug_print("not here yet")
        lin_command, ang_command = inv_kin(lin_speed,ang_speed)
        debug_print([lin_command,ang_command])
        set_speed(dxl_io,[lin_command, ang_command])
    else:
        last_ang_speed += K_ang * (final_angle - error_vector_pos[1])% 360
        lin_command, ang_command = inv_kin(0,last_ang_speed)
        set_speed([lin_command,ang_command])

def asserv(target_pos: tuple[float,float,float],dxl_io):
    err_vect = update_error_vector(get_current_pos(),target_pos)
    debug_print("err_vect")
    debug_print(err_vect)
    set_command(err_vect,target_pos[2],dxl_io)