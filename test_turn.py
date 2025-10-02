from step_motors.goto import turn, move
from step_motors.goto2 import turn_line
from step_motors.setup import setup_motors

## DEBUG ##
DEBUG = 0 # 1 to enable debug_print 0 to deactivate
def debug_print(*args):
    if DEBUG:
        print(*args)



if __name__ == '__main__':
    debug_print("Setting up motors")
    dxl_io = setup_motors()
    turn_line(dxl_io, 2, 5, 0.1)
    #move(dxl_io, 10)
    debug_print("Finished turning")
