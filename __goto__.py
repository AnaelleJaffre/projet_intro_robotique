import numpy as np
import step_motors.goto2 as goto
import step_motors.setup as setup
import time 
## things to remember ##
# distances in meters
# angles in degrees

f_ech = 100 #work frequency in Hz

def main():
   #Setup
   dxl_io = setup.setup_motors()
   while True:
      goto.asserv([0.1,0.1,0],dxl_io)
      time.sleep(1/f_ech)

if __name__ == '__main__':
    main()
