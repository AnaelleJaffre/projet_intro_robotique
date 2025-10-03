import numpy as np
import time
import pypot.dynamixel
import step_motors.odom as odom

## DEBUG ##
DEBUG = 1 # 1 to enable print 0 to deactivate
def debug_print(*args):
    if DEBUG:
        print(*args, flush=True)

# geometric parameters
Rwheels = 25.85*0.001; # wheel radius in m
Drob = 117.2*0.001; # space between both wheels in m

# control parameters 
adressMotorLeft = 1
adressMotorRight = 2

omegaMotorMove = 220 # angular speed in °/s (ie base moves 10 cm/s)
omegaMotorTurn = 202 # angular speed in °/s (ie base turns 90 °/s )
satisfactory_area = 0.01 # circle around target in m

# corr parameters
K_lin = 0.5 #Hz
K_ang = 0.5 #Hz

lin_speed = 0
ang_speed = 0
last_ang_speed = 0


def inv_kin(V,O): # V in m/s and O in °/s
    '''Inverse kinematics: from linear and angular speed to wheel speeds'''
    speedLeft = 180/np.pi * V/Rwheels + Drob/(2*Rwheels)*O
    speedRight = 180/np.pi * V/Rwheels - Drob/(2*Rwheels)*O
    return([speedLeft,speedRight])


def set_speed(dxl_io,command: tuple[float,float]):
    '''Set the speed of the motors'''
    dxl_io.set_moving_speed({adressMotorLeft: command[0]}) 
    dxl_io.set_moving_speed({adressMotorRight: -command[1]}) # Hardware: wheels are opposed


def turn_line(dxl_io, dY, K_cor, V0):
    '''Turn the robot to follow the line'''
    V_MAX = 0.5
    Omega = K_cor * dY # the more the gap the more the angular correction
    # Vlin = np.min(0.1, V0/dY) # the more the gap the less the linear speed, min function to cap Vlin in straight lines
    Vlin = V0 # the more the gap the slower we go
    debug_print("Omega ", Omega) 
    debug_print("Vlin ", Vlin)

    SL, SR = inv_kin(Vlin, Omega)
    # debug_print("SL ", SL)
    # debug_print("SR ", SR)
    set_speed(dxl_io, [SL, SR])


def update_error_vector(current_pos: tuple[float,float,float], target_pos: tuple[float,float,float]): #error vector
    '''Compute the error vector between current position and target position'''
    eps_L = np.sqrt((target_pos[0]-current_pos[0])**2 + (target_pos[1]-current_pos[1])**2)
    eps_T = np.rad2deg(-np.arctan2(target_pos[0]-current_pos[0],target_pos[1]-current_pos[1]))-current_pos[2]
    debug_print(f"Expected rotation : {eps_T} deg")
    return([eps_L, eps_T])


def set_command(error_vector_pos: tuple[float, float], final_angle, dxl_io):
    '''Set the command of the motors based on the error vector'''
    global lin_speed, ang_speed, last_ang_speed

    lin_speed = K_lin * error_vector_pos[0]
    ang_speed = K_ang * error_vector_pos[1]

    # If far from target position, keep moving forward and correct angle
    if (error_vector_pos[0] > satisfactory_area):
        debug_print("not here yet")
        # !TEST! does it word without the - ang_speed ?
        speedLeft , speedRight = inv_kin(lin_speed, ang_speed)
        debug_print("speed command :", [speedLeft, speedRight])
        set_speed(dxl_io,[speedLeft, speedRight])
    
    # If close to target position, stop and correct angle only
    else:
        debug_print("arrived")
        last_ang_speed += K_ang * (final_angle - error_vector_pos[1]) # % 360
        speedLeft, speedRight = inv_kin(0,last_ang_speed)
        set_speed(dxl_io,[speedLeft,speedRight])


def asserv(target_pos, f_ech, dxl_io):
    '''Main asserv loop'''
    robot_pos = odom.get_odom(f_ech,dxl_io)
    debug_print("robot pos :",robot_pos)
    eps_vect = update_error_vector(robot_pos, target_pos)
    debug_print("eps_vect :",eps_vect)
    set_command(eps_vect, target_pos[2], dxl_io)
    
