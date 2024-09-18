"""
----------------------player.py-----------------------------------
o This file is to hold the data for the human player
o Last Modified - September 16th 2024
------------------------------------------------------------------
"""
# libraries
import pygame

# local file specific attribute imports
from helper_funcs import reformat_piece_collision
from piece import Piece, PieceCollisionSize, PieceType, PlayerPiecePosition

# Player class to define a player in Janggi
class Player():

	# Class Initializer
	# INPUT: Side for player (Cho/Han)
	# OUTPUT: Player has side chosen, a var for click state, and a list containing all 
	# 				their Piece objects need for the game
	def __init__(self, color="Cho"):
		self.color = color
		self.is_clicked = False
		self.pieces = self.fill_pieces()

	# Method to populate the player's pieces for Janggi
	# INPUT: None
	# OUTPUT: A list of the piece objects
	def fill_pieces(self):
		pieces = [] # store the piece objects

		# for each piece in PieceType(enum) list
		for piece_type in PieceType:
			# lookup the list of starting positions based on the enum PieceType
			positions = PlayerPiecePosition[piece_type.name].value
			# iterate through that list of starting positions
			for pos in positions:
				# assign point value to current piece based on PieceType(enum)
				point_value = PieceType[piece_type.name].value
				# assign the location that piece will be nad where to display its image
				location = pos
				image_location = pos
				# create a collision rectangle using the enum size for collisions based
				collision_rect = pygame.Rect(pos[0], pos[1],
																		 PieceCollisionSize[piece_type.name].value[0], 
																		 PieceCollisionSize[piece_type.name].value[1])
				# center the rectangle to fit appropriately onto the board
				collision_rect = reformat_piece_collision(location, collision_rect)
				# create the piece based on those parameters
				piece = Piece(piece_type, location, image_location, collision_rect, point_value)
				# add to the list to return
				pieces.append(piece)
		return pieces
