import cv2
import numpy as np
from image_processing.shape_detection import center_of_zone_bis
from step_motors import pos_abs
from step_motors.goto import turn
from step_motors.setup import setup_motors, motors_speed
from image_processing.opencv_inrange_camera_params import RED1, RED2, YELLOW1, YELLOW2, BLUE1, BLUE2, BROWN
from image_processing.shape_rendering import shape_rendering

s_color_order = "b", "r", "y"
color_order = [BLUE1,RED1,YELLOW1]
current_color = 0
robot_poses = []

def main():
    global current_color
    # Get Video Output
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("cam not opened")
        exit()
    
    # Setup motors
    dxl_io = setup_motors()
    motors_speed(dxl_io, 100)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # ROI extraction
        height, width = frame.shape[:2]
        row_position = int(height * 0.3) 
        strip_height = 20

        # save current location in mapping for current color
        robot_poses.append((
            *pos_abs.get_odom()[:2],
            s_color_order[current_color]
        ))
        
        # Get the region of interest (ROI)
        roi = frame[row_position:row_position + strip_height, :]
        cv2.imshow("roi",roi)
        # Convert to HSV and threshold
        
        frame_HSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(frame_HSV, color_order[current_color][0], color_order[current_color][1])
        #Brown detection
        frame_brown = cv2.inRange(frame_HSV, BROWN[0], BROWN[1])
        if cv2.countNonZero(frame_brown) > 0:
            current_color += 1
            if current_color == 3:
                # finished doing all paths, stop robot
                motors_speed(dxl_io, 0)
                break
            
        
        # Get center of zone
        line_follow_point = center_of_zone_bis(frame_threshold, 0, frame_threshold.shape[0]-1)
        
        # Adjust point coordinates to original frame
        line_follow_point_global = [line_follow_point[0], line_follow_point[1] + row_position]
        center_x = width // 2
    
        offset_angle = np.atan2(line_follow_point_global[1] - center_x, line_follow_point_global[0] - center_x)
        print(offset_angle)
        #Adjust motors
        
        turn(dxl_io, offset_angle)
        
        
        # Break if q pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Mapping
    shape_rendering()
    
    cap.release()
    cv2.destroyAllWindows()