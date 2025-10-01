import cv2
import numpy as np
from image_processing.shape_detection import center_of_zone_bis

# Define red color thresholds in HSV
red_lower1 = np.array([0, 100, 100])
red_upper1 = np.array([10, 255, 255])
red_lower2 = np.array([160, 100, 100])
red_upper2 = np.array([180, 255, 255])

if __name__ == '__main__':
    # Get Video Output
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("cam not opened")
        exit()
    
    # For tracking history
    trajectory = []
    max_trajectory_points = 50
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # ROI extraction
        height, width = frame.shape[:2]
        row_position = int(height * 0.3) 
        strip_height = 50
        
        
        # Get the region of interest (ROI)
        roi = frame[row_position:row_position + strip_height, :]
        
        # Convert to HSV and threshold
        frame_HSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(frame_HSV, red_lower1, red_upper1) + \
                         cv2.inRange(frame_HSV, red_lower2, red_upper2)
        
        # Get center of zone
        line_follow_point = center_of_zone_bis(frame_threshold, 0, frame_threshold.shape[0]-1)
        
        # Adjust point coordinates to original frame
        line_follow_point_global = [line_follow_point[0], line_follow_point[1] + row_position]
        center_x = width // 2
        #???????
        offset_angle = np.atan2(line_follow_point_global[1] )

        #Adjust motors
        
        
        # Break if q pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()