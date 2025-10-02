import time

import cv2
import numpy as np
from image_processing.shape_detection import center_of_zone, zone_segment_by_height, center_of_zone_butter
from step_motors import odom
from step_motors.goto import turn
from step_motors.goto import turn_line
from step_motors.setup import setup_motors, motors_speed
from image_processing.opencv_inrange_camera_params import RED, BLUE, YELLOW, BROWN
from image_processing.shape_rendering import shape_rendering

s_color_order = "r", "b", "y"
color_order = [YELLOW, BLUE, RED]
current_color = 0
robot_poses = []
SAMPLING_FREQ_MS = 0.016
PIXEL_TO_MM = 0.3125  # 1 pixel = 0.3125 mm
CONSTANT_LINEAR_SPEED = 100

class MappingSaver:

    def __init__(self):
        self.last_save = time.perf_counter()
        self.robot_poses = []

    def save(self, xy, offset_angle=0, lateral_error=0):
        now = time.perf_counter()
        if now - self.last_save > 1:
            corrected_x = xy[0] - lateral_error * np.sin(offset_angle)
            corrected_y = xy[1] + lateral_error * np.cos(offset_angle)
            xy = (corrected_x*1000, corrected_y*1000) # Convert to mm

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
        print("cam not opened")
        exit()
    
    # Setup motors
    dxl_io = setup_motors()
    #motors_speed(dxl_io, CONSTANT_LINEAR_SPEED)
    
    while True:
        t_start = time.perf_counter()

        ret, frame = cap.read()
        if not ret:
            print("could not fetch frame")
            continue
    

        # save current location in mapping for current color
        mapping_saver.save(odom.get_odom(SAMPLING_FREQ_MS, dxl_io)[:2])

        
        # Convert to HSV and threshold
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(frame_HSV, color_order[current_color][0], color_order[current_color][1])
        
        line_center = center_of_zone(frame_threshold)
        line_center_zone_better = center_of_zone_butter(frame_threshold)

        # Brown detection
        frame_brown = cv2.inRange(frame_HSV, BROWN[0], BROWN[1])
        #if cv2.countNonZero(frame_brown) > 0:
            #current_color += 1
            #if current_color == 3:
                # finished doing all paths, stop robot
                #motors_speed(dxl_io, 0)
                #break
        
        # Get center of zone

        center =  frame.shape[0] / 2

        #cv2.circle(frame, line_center, 5, (0, 255, 0), 2)
        #cv2.imshow("frame", frame)
        # Error angle
        dx = center - line_center_zone_better
        print(dx)

        # Saving position for mapping
        # lateral_error = PIXEL_TO_MM * lateral_error_pixels  # Conversion pixels -> real distance (to adjust)
        robot_xy = odom.get_odom(SAMPLING_FREQ_MS, dxl_io)[:2]
        mapping_saver.save(robot_xy, line_center, dx)
        
        
        # Adjust motors
        turn_line(dxl_io, -dx, CONSTANT_LINEAR_SPEED,  1.0) #dx must be negative for the angular speed to be correct

        elapsed = time.perf_counter() - t_start
        if elapsed < SAMPLING_FREQ_MS:
            time.sleep(SAMPLING_FREQ_MS - elapsed)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    
    # Mapping
    shape_rendering()
    
    cap.release()
    print(robot_poses)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
