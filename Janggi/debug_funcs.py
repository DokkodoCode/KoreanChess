"""
----------------------debug_funcs.py--------------------------------
o This file is to hold any debugging functions for testing
o Last Modified - November 11th 2024
------------------------------------------------------------------
"""

import pygame

# local file imports, see individ file for details
import constants

#-----------------------------------------------------------------------------------
# Function that will render the possible move spots for debugging purposes
# INPUT: Pygame surface object, set of tuples containing coordinates
# OUTPUT: All move-to spots are highlighted for debugging purposes
#-----------------------------------------------------------------------------------
def render_possible_spots(window, spots):
	for move in spots:
		if move is not None:
			rectangle = (move[0], move[1], constants.spot_collision_size[0], 
						 constants.spot_collision_size[1])
			# render the center spots
			pygame.draw.rect(window, constants.GREEN, rectangle)
		
#-----------------------------------------------------------------------------------
# Function that will render aspot onto the center of the screen
# INPUT: display window
# OUTPUT: rectangle rendered at center
#-----------------------------------------------------------------------------------
def render_center(window):
	rectangle = (constants.screen_width/2, constants.screen_height/2, constants.spot_collision_size[0], 
				 constants.spot_collision_size[1])
	# render the palace spots
	pygame.draw.rect(window, constants.GREEN, rectangle)
	return

#-----------------------------------------------------------------------------------
# Function that will render the palaces for DEBUG purposes
# INPUT: display window, board
# OUTPUT: Palace is highlighted for debugging purposes
#-----------------------------------------------------------------------------------
def render_palace_debug(window, board):
	# go to each spot in the palace for cho
	for row in board.bottom_palace:
		for spot in row:
			# define rectangle bounds
			rectangle = (spot[0], spot[1], constants.spot_collision_size[0], 
						 constants.spot_collision_size[1])
			# render the palace spots
			pygame.draw.rect(window, constants.GREEN, rectangle)

	# go to each spot in the palace for han
	for row in board.top_palace:
		for spot in row:
			# define rectangle bounds
			rectangle = (spot[0], spot[1], constants.spot_collision_size[0], 
						 constants.spot_collision_size[1])
			# render the palace spots
			pygame.draw.rect(window, constants.GREEN, rectangle)
	return

#-----------------------------------------------------------------------------------
# Function that will render a spot onto the screen
# INPUT: display window
# OUTPUT: rectangle rendered on screen at coord
#-----------------------------------------------------------------------------------
def render_spot(window, coord, color):
	rectangle = (coord[0], coord[1], constants.small_collision_size[0], 
				 constants.small_collision_size[1])
	pygame.draw.rect(window, color, rectangle)
	return