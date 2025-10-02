from step_motors.goto import turn, move
from step_motors.goto2 import turn_line
from step_motors.setup import setup_motors

if __name__ == '__main__':
    print("Setting up motors")
    dxl_io = setup_motors()
    turn_line(dxl_io, 2, 5, 0.1)
    #move(dxl_io, 10)
    print("Finished turning")
