import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import numpy as np
import time
from image_processing.opencv_inrange_camera_params import BROWN
from image_processing.shape_detection import brown_detection

DEBUG = 1
def debug_print(*args):
    if DEBUG:
        print(*args)

def main():
    # Open camera
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    if not cap.isOpened():
        debug_print("Camera not opened")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            debug_print("Failed to read frame")
            continue

        # Convert to HSV and threshold for brown
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_brown = cv2.inRange(frame_HSV, BROWN[0], BROWN[1])

        # Run brown detection
        detected = brown_detection(frame_brown, threshold=70)

        if detected:
            debug_print("Brown detected!")

        # Show the threshold image
        cv2.imshow("Brown Mask", frame_brown)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
