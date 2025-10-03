import numpy as np
import time
import step_motors.odom as odom
import step_motors.setup as setup
import os

## things to remember ##
# distances in meters
# angles in degrees

## DEBUG ##
DEBUG = 1 # 1 to enable debug_print 0 to deactivate
def debug_print(*args):
    if DEBUG:
        print(*args)


mode = 0 #if mode = 0 then raw angle is tethaK-tethaK-1 if mode = 1 raw angle is omegaMot/f
f_ech = 10 #Hz

def main():
    #Setup
    dxl_io = setup.setup_motors()
    dxl_io.disable_torque({1:0, 2:0})
    while True :
        start = time.perf_counter()


        x, y, theta = odom.get_odom(f_ech, dxl_io)

        debug_print("{:.2f}, {:.2f}, {:.2f}".format(x, y, theta))
        elapsed = time.perf_counter() - start
        if elapsed < 1/f_ech:
            time.sleep((1/f_ech) - elapsed)

if __name__ == "__main__":
    main()
