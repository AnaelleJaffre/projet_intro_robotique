import cv2 as cv
import numpy as np

## DEBUG ##
DEBUG = 0 # 1 to enable debug_print 0 to deactivate
def debug_print(*args):
    if DEBUG:
        print(*args)

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
            debug_print("contour found")
            return [cx, cy]
        else:
            return [img.shape[1] // 2, img.shape[0] // 2]
    else:

        return [img.shape[1] // 2, img.shape[0] // 2]


def center_of_zone_butter(img):
    """compute center of zone using start and end zones"""
    X_STEP = 10
    Y_STEP = 6

    height, width = img.shape
    start = height - 40
    end = height - 40 + Y_STEP

    img_rows = img[start:end, :]

    splits = np.hsplit(img_rows, width / X_STEP)
    avgs = [np.mean(s) for s in splits]

    idx_first_max = np.argmin(avgs)
    idx_last_max = (len(avgs) - 1 - int(np.argmin(avgs[::-1])))

    # for i in range(0, width // X_STEP):
    #     mean = compute_mean(img, x, y)
    #     means.append(mean)
    #     x += X_STEP

    # counter = 0
    # while means[counter] < 100:
    #     counter += 1

    # val_y1 = means[counter] * X_STEP  # Gives the first white segment
    #
    # while means[counter] > 100:
    #     counter += 1
    #
    # val_y2 = means[counter - 1] * X_STEP  # Gives the last white segment

    debug_print(f"({idx_first_max}, {idx_last_max})")
    center = ((idx_first_max + idx_last_max) * X_STEP/ 2, start)

    return center[0]


if __name__ == '__main__':
    cap = cv.VideoCapture(2)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
    win_name = "main"
    cv.namedWindow(win_name)
    _, frame = cap.read()
    # frame = cv.imread("capture_camera.jpg") # height, width, dims (or colors)

    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # lower = (0, 0, 0)
    # higher = (166, 255, 255)
    from opencv_inrange_camera_params import BLUE
    frame_threshold = cv.inRange(frame_HSV, *BLUE)

    debug_print(center_of_zone_butter(frame_threshold))

    line_center_zone_better = center_of_zone_butter(frame_threshold)
    center = frame.shape[0] / 2
    dx = center - line_center_zone_better
    debug_print(f"center: {center}")
    debug_print(f"line_center_zone_better: {line_center_zone_better}")
    debug_print(f"dx: {dx}")

    cv.imshow(win_name, frame_threshold)
    key = cv.waitKey()
