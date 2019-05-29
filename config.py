"""
    A configuration file for the settings to be used for the game.
"""

from pathlib import Path

# Establish window resolution (x, y)
DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 700
RESOLUTION = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

# Establish FPS (frames-per-second) and time delta
FPS = 60
time_delta = 1/FPS

# Establish colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font sizes
default_font_size = 20

# File paths
image_player_car = str(Path("Images/orange_car.png"))
image_enemy_car = str(Path("Images/gray_car.png"))
