import cv2
from image_processing.shape_detection import *

if __name__ == '__main__':
    # Main Loop
    cap = cv2.VideoCapture(0)
    
    while True:
        #image processing
        ret, frame = cap.read()
        if not ret:
            break
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(frame_HSV, (0, 0, 0), (166, 255, 255))
        zones = zone_segment_by_height(frame_threshold)
        centers = [center_of_zone(frame_threshold, *height_bounds) for height_bounds in zones]
        x = [c[0] for c in centers]
        y = [c[1] for c in centers]
        cv2.drawKeypoints(frame, np.array(centers), np.array(centers), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow('frame', frame)
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()