"""
----------------------baord.py----------------------------
o This file is to manage the board object for Janggi
o Last Modified - November 11th 2024
----------------------------------------------------------
"""

# libraries
import pygame
import numpy as np
# local file imports, see individ file for details
import constants
import helper_funcs

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
		self.bottom_palace = [row[-3:] for row in self.coordinates[3:6]]
		self.bottom_palace_collisions = self.cho_assign_palace_collision_spots()
		self.top_palace = [row[:3] for row in self.coordinates[3:6]]
		self.top_palace_collisions  = self.han_assign_palace_collision_spots()
		self.collisions = self.assign_collision_spots()
		self.clear_board_as_array_of_strings()

	def cho_assign_palace_collision_spots(self):
		collision_rects = [] # hold the collision rectangles

		# create a collision rectangle based on the coordinates of the board
		for row in self.bottom_palace:
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
		for row in self.top_palace:
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

	def clear_board_as_array_of_strings(self):
		# Create a template for the board
		self.board_as_array_of_strings = np.array([
			[".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", "."] ])
	
	def add_pieces_to_board(self, player):
		# Some pieces need alias for stockfish
		piece_type_mapping = {
			"Chariot": "R",
			"Elephant": "E",
			"Horse": "H",
			"Pawn": "P",
			"King": "K",
			"Advisor": "A",
			"Cannon": "C"
		}

		row_len = range(len(self.coordinates))
		col_len = range(len(self.coordinates[0]))
		for row in row_len:
			for column in col_len:
				for piece in player.pieces:
					if self.coordinates[row][column] == piece.location:
						self.board_as_array_of_strings[column][row] = piece_type_mapping.get(piece.piece_type.value).lower()

	def update_board_pieces(self, host, guest):
		self.clear_board_as_array_of_strings()
		self.add_pieces_to_board(host)
		self.add_pieces_to_board(guest)

	# Function to generate FEN string from the board state
	# The FEN string is a way of recording the current board state in string format.
	# This string format is what is passed to stockfish so that it can make a move.
	def get_fen(self, player):
		if player.color == 'Cho':
			color = 'b'
		elif player.color == 'Han':
			color = 'w'

		fen_rows = []
		for row in self.board_as_array_of_strings:
			fen_row = ""
			empty_count = 0
			for piece in row:
				if piece == ".":
					empty_count += 1
				else:
					if empty_count > 0:
						fen_row += str(empty_count)
						empty_count = 0
					fen_row += piece
			if empty_count > 0:
				fen_row += str(empty_count)
			fen_rows.append(fen_row)
		
		fen_string = "/".join(fen_rows) + " " + color
		return fen_string


