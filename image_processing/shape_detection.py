import cv2 as cv
import numpy as np

NUM_ZONES = 15
"""Number of zones used during zone segmentation"""

def zone_segment_by_height(img: cv.Mat):
    """Gives a list of tuple of indexes used to segment in NUM_ZONES the image"""
    img_height = img.shape[0]
    sep = int(img_height / NUM_ZONES)
    heights = [i for i in range(0, img_height, sep-1)]
    return [(heights[i] , heights[i+1]) for i in range(len(heights)-1)]


def center_of_zone(img, h_start, h_end):
    """compute center of zone using start and end zones"""
    # for the end, we reverse the array, take the maximum, and compute its location
    z_start = (np.argmin(img[h_start]), img.shape[1] - 1 - np.argmin(img[h_start][::-1]))
    z_start_center = np.min(z_start) + np.abs(z_start[0] - z_start[1]) / 2
    z_end = (np.argmin(img[h_end]), img.shape[1] - 1 - np.argmin(img[h_end][::-1]))
    z_end_center = np.min(z_end) + np.abs(z_end[0] - z_end[1]) / 2

    return np.array((
        (z_start_center + z_end_center) / 2,
        (h_end + h_start) / 2.
    ))

    
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
