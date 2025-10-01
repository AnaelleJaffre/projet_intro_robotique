import numpy as np
import step_motors.goto as goto
import step_motors.setup as setup
## things to remember ##
# distances in meters
# angles in degrees


def main():
   #Setup
   dxl_io = setup.setup_motors()
   goto.goTo(dxl_io,-1,-1,90)
   
   #Close motors
   dxl_io.close()