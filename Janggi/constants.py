"""
----------------------constants.py--------------------------------
o This file is to hold any global constants to be used by program
o Place all global constants into here
o Last Modified - September 24th 2024
------------------------------------------------------------------
"""

# collision sizes for...
spot_collision_size = (60, 60) # board spots

small_collision_size = (50, 50) # small piece collision rects
small_size = (75, 75) # small piece images

med_collision_size = (75, 75) # medium piece collision rects
med_size = (100,100) # medium piece images

large_collision_size = (90, 90) # large piece collision rects
large_size = (125,125) # large piece images

# rectangle colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (100,100,100)
RED = (200,16,46)
BLUE = (0,47,108,)
GREEN = (30,100,0)
LIGHT_GREEN = (35,200,0)

# list of intersectional spaces on Janggi board...
x_coordinates = [82, 179, 276, 373, 470, 567, 664, 761, 858]
y_coordinates = [37, 128, 219, 312, 403, 494, 586, 677, 770, 862]


# game window dimensions (WxH)
window_width = 1000
window_height = 1000

# board size (L, W)
board_size = (900, 900)

# board topleft starting location in window (x, y)
board_image = (50, 50)

# possible settings for checking if a settings pre-set file is correctly written
possible_colorside = ("Cho", "Han")
possible_piece_convention = ("Standard", "International")
possible_ai_level = ("Easy", "Medium", "Hard")