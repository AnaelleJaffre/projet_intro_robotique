import cv2
import numpy as np
from image_processing.shape_detection import center_of_zone

# Define red color thresholds in HSV
# Red wraps around in HSV, so we need two ranges
red_lower1 = np.array([0, 100, 100])      # Lower red range
red_upper1 = np.array([10, 255, 255])
red_lower2 = np.array([160, 100, 100])    # Upper red range  
red_upper2 = np.array([180, 255, 255])

if __name__ == '__main__':
    #### ENORME TEST PAS FINAL DU TOUT ####
    frame = cv2.imread('image_processing/camera_shot.jpg')
    height, width = frame.shape[:2]
    row_position = int(height * 0.3) 
    strip_height = 20
    
    #Range of interest
    roi = frame[row_position:row_position + strip_height, :]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    mask1 = cv2.inRange(hsv_roi, red_lower1, red_upper1)
    mask2 = cv2.inRange(hsv_roi, red_lower2, red_upper2)
    red_mask = cv2.bitwise_or(mask1, mask2)
    
    #clean up
    kernel = np.ones((3, 3), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    
    
    h_start = 0
    h_end = roi.shape[0] - 1
    
    line_follow_point = center_of_zone(red_mask, h_start, h_end)
    
    # Convert to integers and adjust for full frame coordinates
    x = int(line_follow_point[0])
    y = int(line_follow_point[1]) + row_position
    
    print(f"Center point: x={x}, y={y}")
    print(f"ROI shape (height, width): {roi.shape[:2]}")

    cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
    cv2.imshow('Frame', frame)
    cv2.imshow('Red Mask', red_mask)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()