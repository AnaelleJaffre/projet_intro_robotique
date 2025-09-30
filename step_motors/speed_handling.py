center = 0

def lower_speed(angle, speed):
    """Lower the speed of the motors when the robot is turning sharply."""
    
    # Turn right
    if angle > center +10:
        left_speed = speed - angle**1.5
        right_speed *= 1/angle

    # Turn left
    if angle < center -10:
        left_speed *=  1/angle
        right_speed = speed - angle**1.5

    return int(left_speed), int(right_speed)
