import numpy as np
import step_motors.goto as goto
import step_motors.setup as setup

if __name__ == '__goto__':
   #Setup
   dxl_io = setup.setup_motors()
   goto.goTo(dxl_io,0,0,90)
   
   #Close motors
   dxl_io.close()