"""
----------------------render_funcs.py-----------------------------
o This file is solely for rendering-based functions to be 
	used by state.py
o Last Modified - September 17th 2024
------------------------------------------------------------------
"""

# libraries
import pygame

# local file imports
import constants
import helper_funcs
from piece import PieceType


#-----------------------------------------------------------------------------------
# Function that will render both player's pieces onto the board
# INPUT: Player object, Opponent Object, pygame surface object
# OUTPUT: All active-in-play pieces will be rendered
#-----------------------------------------------------------------------------------
def render_pieces(player, opponent, window):
	# load Han-side piece images
	han_piece_images = {
		PieceType.KING: pygame.image.load("Pieces/Han_King.png").convert_alpha(),
		PieceType.ADVISOR: pygame.image.load("Pieces/Han_Advisor.png").convert_alpha(),
		PieceType.ELEPHANT: pygame.image.load("Pieces/Han_Elephant.png").convert_alpha(),
		PieceType.HORSE: pygame.image.load("Pieces/Han_Horse.png").convert_alpha(),
		PieceType.CANNON: pygame.image.load("Pieces/Han_Cannon.png").convert_alpha(),
		PieceType.CHARIOT: pygame.image.load("Pieces/Han_Chariot.png").convert_alpha(),
		PieceType.PAWN: pygame.image.load("Pieces/Han_Pawn.png").convert_alpha()
	}

	# load Cho-side piece images
	cho_piece_images = {
		PieceType.KING : pygame.image.load("Pieces/Cho_King.png").convert_alpha(),
		PieceType.ADVISOR : pygame.image.load("Pieces/Cho_Advisor.png").convert_alpha(),
		PieceType.ELEPHANT: pygame.image.load("Pieces/Cho_Elephant.png").convert_alpha(),
		PieceType.HORSE: pygame.image.load("Pieces/Cho_Horse.png").convert_alpha(),
		PieceType.CANNON: pygame.image.load("Pieces/Cho_Cannon.png").convert_alpha(),
		PieceType.CHARIOT: pygame.image.load("Pieces/Cho_Chariot.png").convert_alpha(),
		PieceType.PAWN: pygame.image.load("Pieces/Cho_Pawn.png").convert_alpha()
	}

	# sizes for the respective piece
	piece_sizes = {
		PieceType.KING: constants.large_size,
		PieceType.ADVISOR: constants.small_size,
		PieceType.ELEPHANT: constants.med_size,
		PieceType.HORSE: constants.med_size,
		PieceType.CANNON: constants.med_size,
		PieceType.CHARIOT: constants.med_size,
		PieceType.PAWN: constants.small_size
	}
	
	# iterate through the opponents's remaining pieces
	# unpack the opponent.pieces into the following:
	# for	PieceType in opponent's active pieces
	for janggi_piece in opponent.pieces:
		piece_image = han_piece_images[janggi_piece.piece_type]
		piece_image = pygame.transform.scale(piece_image,
																				 piece_sizes[janggi_piece.piece_type])
		# center the image correctly to its spot
		piece_image_pos = helper_funcs.reformat_piece(janggi_piece.image_location, piece_image)
		window.blit(piece_image, piece_image_pos)

	# iterate through the player's remaining pieces
	# unpack the player.pieces into the following:
	# for	PieceType, PieceCount, PlayerPiecePosition in player's active pieces
	for janggi_piece in player.pieces:
		piece_image = cho_piece_images[janggi_piece.piece_type]
		piece_image = pygame.transform.scale(piece_image,
																					 piece_sizes[janggi_piece.piece_type])
		# center the image correctly to its spot
		piece_image_pos = helper_funcs.reformat_piece(janggi_piece.image_location, piece_image)
		window.blit(piece_image, piece_image_pos)
	return
	
#-----------------------------------------------------------------------------------
# Function that will render both player's collision boxes of pieces onto the board
# INPUT: Player object, Opponent Object, pygame surface object
# OUTPUT: All active-in-play piece collision rectangles will be rendered
#-----------------------------------------------------------------------------------
def render_piece_collisions(player, opponent, window):
	# render opponent-side collision rects
	for janggi_piece in opponent.pieces:
		pygame.draw.rect(window, constants.RED, janggi_piece.collision_rect)

	# render player-side collision rects
	for janggi_piece in player.pieces:
		if not janggi_piece.is_clicked:
			pygame.draw.rect(window, constants.BLUE, janggi_piece.collision_rect)
		else: # highlight a clicked piece
			pygame.draw.rect(window, constants.LIGHT_GREEN, janggi_piece.collision_rect)
	return
	
#-----------------------------------------------------------------------------------
# Function that will render the possible move spots on the board for a clicked piece
# INPUT: Player object, Opponent Object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_possible_spots(player, board, window):
	# determine the type of piece being moved
	for janggi_piece in player.pieces:
		if janggi_piece.is_clicked:
			match janggi_piece.piece_type.value:
				case "King":
					render_king_possible_spots(janggi_piece, player, board, window)
	
				case "Advisor":
					render_advisor_possible_spots(janggi_piece, player,  board, window)
	
				case "Elephant":
					render_elephant_possible_spots(janggi_piece, player,  board, window)
	
				case "Horse":
					render_horse_possible_spots(janggi_piece, player,  board, window)
	
				case "Cannon":
					render_king_possible_spots(janggi_piece, player,  board, window)
	
				case "Chariot":
					render_chariot_possible_spots(janggi_piece, player,  board, window)
	
				case "Pawn":
					render_pawn_possible_spots(janggi_piece, player,  board, window)
	
				case _:
					raise ValueError("Invalid piece type")
					
	return

#-----------------------------------------------------------------------------------
# Function that will render the possible move spots on the board for the king piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_king_possible_spots(janggi_piece, player, board, window):
	# implement logic here
	return

#-----------------------------------------------------------------------------------
# Function that will render the possible move spots on the board for advisor piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_advisor_possible_spots(janggi_piece, player, board, window):
	# implement logic here
	return

#-----------------------------------------------------------------------------------
# Function that will render the possible move spots on the board for elephant piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_elephant_possible_spots(janggi_piece, player, board, window):
	# implement logic here
	return

#-----------------------------------------------------------------------------------
# Function that will render the possible move spots on the board for the horse piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_horse_possible_spots(janggi_piece, player, board, window):
	# implement logic here
	return

#-----------------------------------------------------------------------------------
# Function that will render possible move spots on the board for the cannon piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_cannon_possible_spots(janggi_piece, player, board, window):
	# implement logic here
	return

#-----------------------------------------------------------------------------------
# Function that will render possible move spots on the board for the chariot piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_chariot_possible_spots(janggi_piece, player, board, window):
	# implement logic here
	return

#-----------------------------------------------------------------------------------
# Function that will render the possible move spots on the board for the pawn piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_pawn_possible_spots(janggi_piece, player, board, window):
	# Possible moves for the piece based on current possition (L/R/U)
	# view board as vertical (standard) where top of board is beginning of
	# the 2D list
	# (-x, y) --> left x spots
	# (+x, y) --> right x spots
	# (x, -y) --> up y spots
	# (x, +y) --> down y spots
	#				[ (Left) , (Right), (Up)  ]
	possible_moves = [(-1, 0), (1, 0), (0, -1)]

	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(board.coordinates):
		for file, spot in enumerate(row):
			# find where piece is relative to board
			if spot == janggi_piece.location:
				# Show where piece can move by looking at each of 
				# the possible locations piece can move
				for move in possible_moves:
					new_rank = rank + move[0]
					new_file = file + move[1]

					# check that move location is within board
					if ((0 <= new_rank < len(board.coordinates))
							and (0 <= new_file < len(row))):
						# take the coords for the spot to potentially highlight
						new_rect = board.collisions[new_rank][new_file]
						
						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece):
							
							# potential jump-to spot found, align the rectangle for drawing
							new_spot = board.coordinates[new_rank][new_file]
							new_spot = helper_funcs.reformat_spot_collision(new_spot,
																			board.collisions[new_rank]
																			[new_file])
							
							# rectangle bounds for drawing the spot rectangle
							rectangle = (new_spot[0], new_spot[1], 
													 constants.spot_collision_size[0], 
													 constants.spot_collision_size[1])
							
							# render the possible spot
							pygame.draw.rect(window, constants.GREEN, rectangle)
	return

#-----------------------------------------------------------------------------------
# Function that will render the palaces for DEBUG purposes
# INPUT: board object, pygame surface object
# OUTPUT: Palace is highlighted for debugging purposes
#-----------------------------------------------------------------------------------
def render_palace_debug(board, window):
	# go to each spot in the palace for cho
	for row in board.cho_palace:
		for spot in row:
			# define rectangle bounds
			rectangle = (spot[0], spot[1], constants.spot_collision_size[0], 
										constants.spot_collision_size[1])
			# render the palace spots
			pygame.draw.rect(window, constants.GREEN, rectangle)

			# go to each spot in the palace for han
	for row in board.han_palace:
		for spot in row:
			# define rectangle bounds
			rectangle = (spot[0], spot[1], constants.spot_collision_size[0], 
										constants.spot_collision_size[1])
			# render the palace spots
			pygame.draw.rect(window, constants.GREEN, rectangle)
	return