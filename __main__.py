import cv2
import numpy as np
import pypot.dynamixel
from step_motors.setup import setup_motors
from image_processing.shape_detection import center_of_zone
from step_motors.speed_handling import lower_speed

prev_pos = [0,0]
# Define red color thresholds in HSV
# Red wraps around in HSV, so we need two ranges
red_lower1 = np.array([0, 100, 100])      # Lower red range
red_upper1 = np.array([10, 255, 255])
red_lower2 = np.array([160, 100, 100])    # Upper red range  
red_upper2 = np.array([180, 255, 255])

if __name__ == '__main__':
    
    #Get Video Output
    cap = cv2.VideoCapture(2)
    dxl_io = setup_motors()
    while True:
        _, frame = cap.read()
        #ROI
        frame = frame[0:480, 0:640]
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(frame_HSV, red_lower1, red_upper1) + cv2.inRange(frame_HSV, red_lower2, red_upper2)
        #cv2.imshow("frame", frame_threshold)
        
        #Get center of zone
        line_follow_point = center_of_zone(frame_threshold, 0, frame_threshold.shape[0]-1)
        print(line_follow_point)
        
        #Move accordingly
        to_angle = np.arctan2(line_follow_point[1] - prev_pos[1], line_follow_point[0] - prev_pos[0])
        prev_pos = line_follow_point
        motor_speed = lower_speed(to_angle, 100)
        
        #adjust motors
        dxl_io.set_moving_speed({1: motor_speed[0]})
        dxl_io.set_moving_speed({2: motor_speed[1]})
        
        #break if q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()