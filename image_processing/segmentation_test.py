import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from shape_detection import *

if __name__ == '__main__':
    img = np.asarray(Image.open("sample_dark_red_line.png"))
    plt.imshow(img)

    zones = zone_segment_by_height(img)
    centers = [center_of_zone(img, *height_bounds) for height_bounds in zones]
    x = [c[0] for c in centers]
    y = [c[1] for c in centers]
    plt.scatter(x, y)
    plt.show()
