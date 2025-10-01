import numpy as np
import time
import pypot.dynamixel
import pos_abs


def error_vector(current_pos: tuple[float,float], target_pos: tuple[float,float]):
    eps_L = target_pos[0]-current_pos[0]
    eps_T = target_pos[1]-current_pos[1]
    return([eps_L,eps_T])

def get_current_pos():
    X,Y,T = pos_abs.get_odom()
    L = np.sqrt(X*X+Y*Y)
    return([L,T])

def set_command(error_vector: tuple[float,float]):
    lin_speed += 