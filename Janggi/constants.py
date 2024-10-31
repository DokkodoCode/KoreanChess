"""
----------------------constants.py--------------------------------
o This file is to hold any global constants to be used by program
o Place all global constants into here
o Last Modified - October 31st 2024
------------------------------------------------------------------
"""
import pygame

# initialize pygame instance
pygame.init()


running = True

# create window size based on user's machine
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
window_width, window_height = screen_width-50, screen_height-50


# board size (L, W)
board_size = (window_height - 50, window_height - 50)

# board topleft starting location in window (x, y)
board_image = (round(screen_width/5), 50)


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

# offsets for creating of intersectional spaces on Janggi board...
x_offset = [40, 145, 250, 355, 460, 565, 670, 775, 880]
y_offset = [-10, 90, 190, 290, 390, 490, 590, 690, 790, 890]

# creating intersectional spaces on Janggi board...
x_coordinates = [round(board_image[0] + offset) for offset in x_offset]
y_coordinates = [round(board_image[1] + offset) for offset in y_offset]

# possible settings for checking if a settings pre-set file is correctly written
possible_colorside = ("Cho", "Han")
possible_piece_convention = ("Standard", "International")
possible_ai_level = ("Easy", "Medium", "Hard")