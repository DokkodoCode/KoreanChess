"""
----------------------player.py-----------------------------------
o This file is to hold the data for the human player
o Last Modified - Novemeber 19th 2024
------------------------------------------------------------------
"""
# libraries
import pygame


# local file imports, see individ file for details
from helper_funcs import reformat_piece_collision, dynamic_scale_x, dynamic_scale_y
import constants
from piece import Piece, PieceCollisionSize, PieceType, PlayerPiecePosition, OpponentPiecePosition

# Player class to define a player in Janggi
class Player():

	# Class Initializer
	# INPUT: Side for player (Cho/Han)
	# OUTPUT: Player has side chosen, the style convention for the pieces they will use, 
	# 		  the level of AI they play agaianst, a var for click state, and a list containing all 
	# 		  their Piece objects need for the game
	def __init__(self, is_host=False, board_perspective="Bottom"):
		self.color = "Cho"
		self.is_host = is_host
		self.board_perspective = board_perspective
		self.piece_convention = "Standard"
		self.ai_level = None
		self.is_ready = False
		self.is_clicked = False
		self.is_turn = False
		self.pieces = self.fill_pieces()
		self.settings = self.initialize_settings()

	# Method to populate the player's pieces for Janggi
	# INPUT: None
	# OUTPUT: A list of the piece objects
	def fill_pieces(self):
		pieces = []  # store the piece objects
		
		# for each piece in PieceType (enum) list
		for piece_type in PieceType:
			# lookup the list of starting positions based on the enum PieceType
			if self.is_host:
				positions = PlayerPiecePosition[piece_type.name].value
			else:
				positions = OpponentPiecePosition[piece_type.name].value
			
			# iterate through that list of starting positions
			for pos in positions:
				# assign point value based on PieceType (enum)
				point_value = PieceType[piece_type.name].value
				
				# assign the base location and image location (both are base coordinates)
				location = pos
				image_location = pos
				
				# retrieve the base collision size from the enum
				collision_size = PieceCollisionSize[piece_type.name].value
				
				# create a collision rectangle using the base values
				collision_rect = pygame.Rect(pos[0], pos[1], collision_size[0], collision_size[1])
				
				# center the collision rectangle onto the board appropriately
				collision_rect = reformat_piece_collision(location, collision_rect)
				
				# create the piece based on these parameters
				piece = Piece(piece_type, location, image_location, collision_rect, point_value)
				
				# *** Store the base (1920x1080) values for later scaling ***
				piece.base_location = pos
				piece.base_image_location = pos
				piece.base_collision_size = collision_size
				
				# add the piece to the list
				pieces.append(piece)
				
		return pieces

	
	def print_pieces(self):
		for piece in self.pieces:
			print(piece.piece_type)

	# Method to populate the player's settings used last game played
	# INPUT: None
	# OUTPUT: Either a new text file is created containing the basic settings, where 
	# 		  each setting is seperated by the delimiter character '|' or the existing
	# 		  text file folowing same delimiter and is valid is used to populate the player's settings
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
			player_settings = ["Cho", "Standard", "Easy"]

			with open(settings_file, 'w') as outfile:
				settings = '|'.join(player_settings)
				outfile.write(settings)
			return player_settings

	# Update each piece’s image location and collision rectangle based on the current window dimensions.
    # This should be called after a window resize.	
	def update_piece_positions(self, window):
		# Set the base resolution used in constants (adjust if your base differs).
		base_width = 1920
		base_height = 1080
		
		current_width, current_height = window.get_size()
		
		for piece in self.pieces:
			# Update the image location by scaling the base image location.
			base_x, base_y = piece.base_image_location
			new_x = dynamic_scale_x(base_x, current_width, base_width)
			new_y = dynamic_scale_y(base_y, current_height, base_height)
			piece.image_location = (new_x, new_y)
			
			# Update the collision rectangle.
			base_coll_size = piece.base_collision_size  # (width, height)
			new_coll_width = dynamic_scale_x(base_coll_size[0], current_width, base_width)
			new_coll_height = dynamic_scale_y(base_coll_size[1], current_height, base_height)
			
			# Create a new rect at the new location with the new size.
			piece.collision_rect = pygame.Rect(new_x, new_y, new_coll_width, new_coll_height)
			
			# Re-center the collision rectangle using your helper (if it applies an offset).
			piece.collision_rect = reformat_piece_collision(piece.image_location, piece.collision_rect, piece.current_width)
