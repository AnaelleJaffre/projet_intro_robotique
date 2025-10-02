import cv2 as cv
import numpy as np

def zone_segment_by_height(img: cv.Mat, NUM_ZONES: int):
    """Gives a list of tuple of indexes used to segment in NUM_ZONES the image"""
    img_height = img.shape[0]
    sep = int(img_height / NUM_ZONES)
    heights = [i for i in range(0, img_height, sep-1)]
    return [(heights[i] , heights[i+1]) for i in range(len(heights)-1)]

def center_of_zone_bis(binary_image, start_row, end_row):
    """Calculate center of detected region (placeholder - replace with your implementation)"""
    # Find contours in the binary image
    contours, _ = cv.findContours(binary_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv.contourArea)
        M = cv.moments(largest_contour)
        
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return [cx, cy]
    
    # Default to center if no contours found
    return [binary_image.shape[1] // 2, binary_image.shape[0] // 2]


def center_of_zone(height, width):
    """compute center of zone using start and end zones"""
    # # for the end, we reverse the array, take the maximum, and compute its location
    # z_start = (np.argmax(img[h_start]), img.shape[1] - 1 - np.argmax(img[h_start][::-1]))
    # z_start_center = np.min(z_start) + np.abs(z_start[0] - z_start[1]) / 2
    # z_end = (np.argmax(img[h_end]), img.shape[1] - 1 - np.argmax(img[h_end][::-1]))
    # z_end_center = np.min(z_end) + np.abs(z_end[0] - z_end[1]) / 2

    # return np.array((
    #     (z_start_center + z_end_center) / 2,
    #     (h_end + h_start) / 2.
    # ))

    x = height-40
    y = 0
    means = []
    center = (height/2, width/2)

    for i in range(0, width//10):
        mean = compute_mean(x, y)
        means.append(mean)
        y += 10
    
    counter = 0
    while means[counter] < 100:
        counter += 1
    
    val_y1 = means[counter]*10 # Gives the first white segment

    while means[counter] > 100:
        counter += 1
    
    val_y2 = means[counter-1]*10 # Gives the last white segment

    center = (x, (val_y1 + val_y2) / 2)

    return center


def compute_mean(x, y):
    mean = 0

    return mean
    
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
