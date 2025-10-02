import numpy as np
import time
import step_motors.odom as odom
import step_motors.setup as setup

## things to remember ##
# distances in meters
# angles in degrees

f_ech = 100 #sampling frequency in Hz 


def main():
    #Setup
    dxl_io = setup.setup_motors()
    while True :
        print(odom.get_odom(f_ech,dxl_io))
        time.sleep(1/f_ech)
    
if __name__ == "__main__":
    main()