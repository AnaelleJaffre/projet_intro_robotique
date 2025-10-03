import time

import cv2
import numpy as np
from image_processing.shape_detection import center_of_zone_butter, brown_detection
#from step_motors import odom
#from step_motors.goto import turn
from step_motors.goto2 import turn_line
from step_motors.setup import setup_motors, motors_speed
from step_motors.odom import get_odom
from image_processing.opencv_inrange_camera_params import RED, BLUE, YELLOW, BROWN
from image_processing.new_params import NEW_BLUE, NEW_RED, NEW_YELLOW, NEW_BROWN
from image_processing.shape_rendering import shape_rendering
import signal
import sys

## DEBUG ##
DEBUG = 1 # 1 to enable debug_print 0 to deactivate
def debug_print(*args):
    if DEBUG:
        print(*args)

s_color_order = "y", "b", "r"
color_order = [YELLOW, BLUE, RED]
current_color = 0
robot_poses = []
SAMPLING_FREQ_MS = 0.016
CONSTANT_LINEAR_SPEED = 100

class MappingSaver:

    def __init__(self):
        self.last_save = time.perf_counter()
        self.robot_poses = []

    def save(self, xy, offset_angle=0, lateral_error=0):
        now = time.perf_counter()
        if now - self.last_save > 0.6: # save every 0.6s
            corrected_x = xy[0]*1000 - lateral_error * np.sin(offset_angle)
            corrected_y = xy[1]*1000 + lateral_error * np.cos(offset_angle)
            xy = (corrected_x, corrected_y)

            self.robot_poses.append((*xy, s_color_order[current_color]))
            self.last_save = now


mapping_saver = MappingSaver()


def main():
    global current_color
    # Get Video Output
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    if not cap.isOpened():
        debug_print("cam not opened")
        exit()
    
    # Setup motors
    dxl_io = setup_motors()
    def stop_motors(_, __):
        dxl_io.set_moving_speed({1:0})
        dxl_io.set_moving_speed({2:0})
        dxl_io.disable_torque([1, 2])
        cap.release()
        exit(0)

    signal.signal(signal.SIGINT, stop_motors)

    #motors_speed(dxl_io, CONSTANT_LINEAR_SPEED)
    
    while True:
        t_start = time.perf_counter()

        ret, frame = cap.read()
        if not ret:
            debug_print("could not fetch frame")
            continue
        
        # Convert to HSV and threshold
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(frame_HSV, color_order[current_color][0], color_order[current_color][1])
        
        #line_center = center_of_zone(frame_threshold)
        line_center_zone_better = center_of_zone_butter(frame_threshold)

        # Brown detection
        frame_brown = cv2.inRange(frame_HSV, BROWN[0], BROWN[1])
        
        
        if(brown_detection(frame_brown, threshold=100)):
            current_color = (current_color + 1)
            debug_print(f"Brown detected, current color: {s_color_order[current_color]}")
            if current_color == len(color_order):
                break
            
        # Get center of zone

        center =  frame.shape[0] / 2
        
        # Visual Debug
        # cv2.circle(frame, line_center, 5, (0, 255, 0), 2)
        # cv2.imshow("frame", frame)
        
        # Error angle
        dx = line_center_zone_better - center
        debug_print(f"dx : {dx}")

        # Saving position for mapping
        robot_xy = get_odom(SAMPLING_FREQ_MS, dxl_io)[:2]
        mapping_saver.save(robot_xy, line_center_zone_better, dx)
        
        # cv2.imshow('frame',frame_threshold)
        # Adjust motors
        turn_line(dxl_io, dx, K_cor=0.75,  V0=0.1) ##dx must be negative for the angular speed to be correct

        elapsed = time.perf_counter() - t_start
        print("time: ", elapsed)
        if elapsed < SAMPLING_FREQ_MS:
            time.sleep(SAMPLING_FREQ_MS - elapsed)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # Mapping
    shape_rendering(mapping_saver.robot_poses)
    debug_print(robot_poses)
    
    # Cleanup
    dxl_io.set_moving_speed({1:0, 2:0})
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
