import cv2
import numpy as np

# Parameters
height = 700
width = 1000

# Functions
def pointing_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        points.append((x, y))
        if len(points) >= 2:
            cv2.line(img, points[-2], points[-1], (255, 0, 0), 5)

# Main
img = np.zeros(shape=(height, width, 3), dtype=np.uint8)
img[:] = [251, 245, 254]  # Background color
points = []
window_name = "image"

cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, pointing_event)

while True:
    cv2.imshow(window_name, img)  # Always refresh window
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cv2.destroyAllWindows()
