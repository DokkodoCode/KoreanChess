"""
----------------------player.py-----------------------------------
o This file is to hold the data for the human player
o Last Modified - October 3rd 2024
------------------------------------------------------------------
"""
# libraries
import pygame


# local file specific attribute imports
from helper_funcs import reformat_piece_collision
import constants
from piece import Piece, PieceCollisionSize, PieceType, PlayerPiecePosition

# Player class to define a player in Janggi
class Player():

	# Class Initializer
	# INPUT: Side for player (Cho/Han)
	# OUTPUT: Player has side chosen, the style convention for the pieces they will use, 
	# 		  the level of AI they play agaianst, a var for click state, and a list containing all 
	# 		  their Piece objects need for the game
	def __init__(self, color="Cho"):
		self.color = color
		self.piece_convention = "Standard"
		self.ai_level = "Easy"
		self.is_clicked = False
		self.pieces = self.fill_pieces()
		self.settings = self.initialize_settings()

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

	# Method to populate the player's settings used last game played
	# INPUT: None
	# OUTPUT: Either a new text file is created containing the basic settings
	#		  or the existing text file that is valid is used to populate the player's settings
	def initialize_settings(self):
		settings_file = "Settings/settings.txt"

		# file may not exist, handle smoothly
		try:
			with open(settings_file) as infile:
				# get the settings from file, and update player vars
				player_settings = infile.readline().strip('\n').split('|')

				# check to make sure settings file format is correct
				if (len(player_settings) == 3
					and player_settings[0] in constants.possible_colorside
					and player_settings[1] in constants.possible_piece_convention
					and player_settings[2] in constants.possible_ai_level):

					# use those settings if valid
					self.color = player_settings[0]
					self.piece_convention = player_settings[1]
					self.ai_level = player_settings[2]

				# otherwise just use the default settings
				else:
					player_settings = [self.color, self.piece_convention, self.ai_level]

				return player_settings
		
		# settings file does not exist, create one using default settings
		except:
			FileNotFoundError
			print("Player's settings file was not found, initialize base settings instead...")
			player_settings = [self.color, self.piece_convention, self.ai_level]

			with open(settings_file, 'w') as outfile:
				settings = '|'.join(player_settings)
				outfile.write(settings)
			return player_settings
