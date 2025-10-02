import numpy as np
# Min for values : 0
# Hue max : 360 // 2
# Other max values : 255

# -- OLD
# RED = (
#     np.array([0, 152, 155]), # Lows
#     np.array([7, 200, 236]) # Highs
# )
#
# YELLOW = (
#     np.array([37, 0, 86]), # Lows
#     np.array([115, 37, 183]) # Highs
# )
#
#
# BLUE = (
#     np.array([20, 0, 109]), # Lows
#     np.array([121, 192, 175]) # Highs
# )
#
#
# BROWN = (
#     np.array([0, 69, 67]), # Lows
#     np.array([82, 151, 144]) # Highs
# )

RED = (
    (0, 64, 0),
    (20, 255, 255)
)

YELLOW, BLUE, BROWN = [None] * 3