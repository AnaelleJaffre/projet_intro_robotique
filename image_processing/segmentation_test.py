import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from shape_detection import *
import cv2 as cv

## DEBUG ##
DEBUG = 0 # 1 to enable debug_print 0 to deactivate
def debug_print(message):
    if DEBUG:
        print(message)



if __name__ == '__main__':
    img = cv.imread("./sample_dark_red_line.png")
    img = img[:, :, :3]

    lower = (0, 0, 0)
    higher = (166, 255, 255)
    frame_threshold = cv.inRange(img, lower, higher)
    plt.imshow(frame_threshold)

    zones = zone_segment_by_height(frame_threshold)
    centers = [center_of_zone(frame_threshold, *height_bounds) for height_bounds in zones]
    x = [c[0] for c in centers]
    y = [c[1] for c in centers]
    debug_print(centers)
    plt.scatter(x, y)

    plt.show()
