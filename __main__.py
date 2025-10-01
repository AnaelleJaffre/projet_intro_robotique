import cv2
from image_processing.shape_detection import *
from step_motors import *
import __line__
import __goto__

# Convert to functions instead of texts
modes = {
    ord('1'): __line__.main(),
    ord('2'): __goto__.main(),
    ord('3'): "launch odometry",
    ord('0'): None
}

if __name__ == '__main__':
    # Main Loop
    cap = cv2.VideoCapture(0)
    current_mode = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        key = cv2.waitKey(1) & 0xFF       
        if key == ord('q'):
            break

        elif key in modes:
            current_mode = modes[key]
            current_mode() 

    cap.release()
    cv2.destroyAllWindows()