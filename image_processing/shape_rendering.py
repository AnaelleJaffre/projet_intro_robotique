import cv2
import numpy as np

example =  [(0, 0, "r"), (20, 100, "r"), (50, 235, "r"), (80, 122, "y"), (343, 162, "y"), (85, 1, "y"), (6, 3, "b"), (27, -10, "b"),  (45, -16, "b"),  (57, -30, "b"),  (48, -60, "b")]  # Example points with colors

def shape_rendering(path_points = example):
    """
    Renders a path defined by a list of points with associated colors onto an image.

    Parameters:
    - path_points: List of tuples (x, y, color) where color is 'r', 'y', or 'b'.

    Returns:
    - img: The rendered image as a NumPy array.
    """

    # Find min/max for each axis
    xs = [p[0] for p in path_points]
    ys = [p[1] for p in path_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Optional margin
    margin = 10

    # Set image size
    width = int(max_x - min_x + 2 * margin)
    height = int(max_y - min_y + 2 * margin)

    # Create a blank image
    img = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    img[:] = [241, 245, 247]  # Background color

    # Scale and shift points to fit image
    def world_to_image(x, y):
        ix = int(x - min_x + margin)
        iy = int(y - min_y + margin)
        return ix, iy

    # Window
    window_name = "image"
    cv2.namedWindow(window_name)

    # Draw path
    for i in range(1, len(path_points)):
        color = path_points[i][2]

        match color:
            case "r":
                color = (0, 0, 255)  # Red in BGR
            case "y":
                color = (0, 255, 255)  # Yellow in BGR
            case "b":
                color = (255, 0, 0)  # Blue in BGR
            case _:
                color = (255, 255, 255)  # Default to white

        # Drawing the line
        pt1 = world_to_image(path_points[i-1][0], path_points[i-1][1])
        pt2 = world_to_image(path_points[i][0], path_points[i][1])
        cv2.line(img, pt1, pt2, color, 2)

    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img
