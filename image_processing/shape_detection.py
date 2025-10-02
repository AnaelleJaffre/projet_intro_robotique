import cv2 as cv
import numpy as np

width_part = 20
height_part = 6
def zone_segment_by_height(img: cv.Mat, NUM_ZONES: int):
    """Gives a list of tuple of indexes used to segment in NUM_ZONES the image"""
    img_height = img.shape[0]
    sep = int(img_height / NUM_ZONES)
    heights = [i for i in range(0, img_height, sep-1)]
    return [(heights[i] , heights[i+1]) for i in range(len(heights)-1)]


def center_of_zone(img):
    """compute center of zone using start and end zones"""
    contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # find the largest contour in the image
        largest_contour = max(contours, key=cv.contourArea)
        M = cv.moments(largest_contour)
        
        # Make sure no countour are without borders
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return [cx, cy]
        else:
            return [img.shape[1] // 2, img.shape[0] // 2]
    else:
        return [img.shape[1] // 2, img.shape[0] // 2]
    
if __name__ == '__main__':
    # cap = cv.VideoCapture(2)
    win_name = "main"
    cv.namedWindow(win_name)
    # _, frame = cap.read()
    frame = cv.imread("image_processing\sample_dark_red_line.png") # height, width, dims (or colors)

    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lower = (0, 0, 0)
    higher = (166, 255, 255)
    frame_threshold = cv.inRange(frame_HSV, lower, higher)

    cv.imshow(win_name, frame_threshold)
    key = cv.waitKey()
