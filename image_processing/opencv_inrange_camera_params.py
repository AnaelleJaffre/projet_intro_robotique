import numpy as np
# Min for values : 0
# Hue max : 360 // 2
# Other max values : 255

RED = (
    np.array([0, 43, 131]), # Lows
    np.array([20, 255, 255]) # Highs
)

YELLOW = (
    np.array([26, 89, 76]), # Lows
    np.array([30, 156, 255]) # Highs
)


BLUE = (
    np.array([0, 0, 73]), # Lows
    np.array([180, 161, 237]) # Highs
)


BROWN = ( 
    np.array([0, 0, 0]), # Lows
    np.array([13, 129, 130]) # Highs
)