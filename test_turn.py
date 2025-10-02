from step_motors.goto import turn
from step_motors.setup import setup_motors

if __name__ == '__main__':
    print("Setting up motors")
    dxl_io = setup_motors()
    turn(dxl_io, 180)
    print("Finished turning")
