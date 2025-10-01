import numpy as np

def lower_speed(angle, speed):
    """Lower the speed of the motors when the robot is turning sharply."""
    angle = np.rad2deg(angle)
    left_speed = speed
    right_speed = speed
    # Turn right
    if angle > 0 +10:
        left_speed = speed - angle**1.5
        right_speed *= 1/angle

    # Turn left
    if angle < 0 -10:
        left_speed *=  1/angle
        right_speed = speed - angle**1.5

    return [int(left_speed), int(-right_speed)]
