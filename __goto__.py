import numpy as np
import step_motors.goto2 as goto
import step_motors.setup as setup
import time
import signal
import sys

    # Setup motors

## things to remember ##
# distances in meters
# angles in degrees
mode = 0 ##if mode = 0 then raw angle is tethaK-tethaK-1 if mode = 1 raw angle is omegaMot/f
f_ech = 10 #work frequency in Hz

def main():
   #Setup
   dxl_io = setup.setup_motors()
   def stop_motors(_, __):
      dxl_io.set_moving_speed({1:0})
      dxl_io.set_moving_speed({2:0})
      dxl_io.disable_torque([1, 2])
      exit(0)

   signal.signal(signal.SIGINT, stop_motors)
   while True:
      goto.asserv([0.1,0.1,0], f_ech, dxl_io)
      time.sleep(1/f_ech)

if __name__ == '__main__':
    main()
