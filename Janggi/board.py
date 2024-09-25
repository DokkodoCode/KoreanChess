"""
----------------------baord.py----------------------------
o This file is to manage the board object for Janggi
o Last Modified - September 17th 2024
----------------------------------------------------------
"""

# libraries
import pygame

# local file imports
import constants
import helper_funcs

# list of cho-side palace square

# Class for Janggi Board
class Board():

	# Class Initializer
	# INPUT: None
	# OUTPUT: 
	#			1) A 2D list of the coordinates of intersections is created
	#			2) a slice of the 2D coordinate list is made for the Cho palace
	#			3) a slice of the 2D coordinate list is made for the Han palace
	#			4) A 2D list of the collision rectangles based on each 
	#				 coordinate is created
	def __init__(self):
		self.coordinates = [[(x,y) for y in constants.y_coordinates]
												for x in constants.x_coordinates]
		self.cho_palace = [row[-3:] for row in self.coordinates[3:6]]
		self.cho_palace_collisions = self.cho_assign_palace_collision_spots()
		self.han_palace = [row[:3] for row in self.coordinates[3:6]]
		self.han_palace_collisions  = self.han_assign_palace_collision_spots()
		self.collisions = self.assign_collision_spots()

	def cho_assign_palace_collision_spots(self):
		collision_rects = [] # hold the collision rectangles

		# create a collision rectangle based on the coordinates of the board
		for row in self.cho_palace:
			row_collision_rects = [] # hold the rectangles in the row

			for coordinate in row:
				# create rectangle
				collision_rect = pygame.Rect(coordinate[0], coordinate[1],
																		 constants.spot_collision_size[0],
																		constants.spot_collision_size[1])
				# center collision rectangle in its spot
				collision_rect = helper_funcs.reformat_spot_collision(coordinate, collision_rect)
				# add to row list
				row_collision_rects.append(collision_rect)
			# add row to list
			collision_rects.append(row_collision_rects)

		return collision_rects
	
	def han_assign_palace_collision_spots(self):
		collision_rects = [] # hold the collision rectangles

		# create a collision rectangle based on the coordinates of the board
		for row in self.han_palace:
			row_collision_rects = [] # hold the rectangles in the row

			for coordinate in row:
				# create rectangle
				collision_rect = pygame.Rect(coordinate[0], coordinate[1],
										constants.spot_collision_size[0],
										constants.spot_collision_size[1])
				# center collision rectangle in its spot
				collision_rect = helper_funcs.reformat_spot_collision(coordinate, collision_rect)
				# add to row list
				row_collision_rects.append(collision_rect)
			# add row to list
			collision_rects.append(row_collision_rects)

		return collision_rects

	# Method to populate the board with collision spots for pieces to jump to
	# INPUT: None
	# OUTPUT: 2D List containing all the collision rectangles for the 
	#				  board spots is created
	def assign_collision_spots(self):
		collision_rects = [] # hold the collision rectangles

		# create a collision rectangle based on the coordinates of the board
		for row in self.coordinates:
			row_collision_rects = [] # hold the rectangles in the row

			for coordinate in row:
				# create rectangle
				collision_rect = pygame.Rect(coordinate[0], coordinate[1],
																		 constants.spot_collision_size[0],
																		constants.spot_collision_size[1])
				# center collision rectangle in its spot
				collision_rect = helper_funcs.reformat_spot_collision(coordinate, collision_rect)
				# add to row list
				row_collision_rects.append(collision_rect)
			# add row to list
			collision_rects.append(row_collision_rects)

		return collision_rects
