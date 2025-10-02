import cv2
from image_processing.shape_detection import *
from step_motors import *
import __line__
import __goto__
import __odom__

# Convert to functions instead of texts
modes = {
    '1': __line__.main,
    '2': __goto__.main,
    '3': __odom__.main,
}

# Selects a mode and launches it
if __name__ == '__main__':
    
    key = input("Choose a mode: \n\n1: Line-Following & Mapping, \n2: Go To, \n3: Odometry, \n0: Exit\n\n")    

    if key in modes:
        modes[key]()
    
    print("Exiting...")