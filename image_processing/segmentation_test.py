import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from shape_detection import *

if __name__ == '__main__':
    img = np.asarray(Image.open("image_processing\sample_dark_red_line.png"))
    plt.imshow(img)

    line_follow_point = center_of_zone(img, 0, img.shape[0]-1)

    x = [line_follow_point[0]]
    y = [line_follow_point[1]]
   
    plt.scatter(x, y)
    plt.show()
