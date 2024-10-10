"""
----------------------render_funcs.py-----------------------------
o This file is solely for rendering-based functions to be 
	used by state.py
o Last Modified - October 3rd 2024
------------------------------------------------------------------
"""

# libraries
import pygame

# local file imports
import constants
import helper_funcs
from piece import PieceType, PreGamePieceDisplay


#-----------------------------------------------------------------------------------
# Function that will render a lineup for viewing of the player's pieces when 
# changing settings for the game
# INPUT: Pygame surface object, player object
# OUTPUT: Piece line-up is rendered during pre-game set-up
#-----------------------------------------------------------------------------------
def PreGame_render_piece_display(window, player):
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

	# load International Han-side piece images
	I_han_piece_images = {
		PieceType.KING: pygame.image.load("Pieces/I_Han_King.png").convert_alpha(),
		PieceType.ADVISOR: pygame.image.load("Pieces/I_Han_Advisor.png").convert_alpha(),
		PieceType.ELEPHANT: pygame.image.load("Pieces/I_Han_Elephant.png").convert_alpha(),
		PieceType.HORSE: pygame.image.load("Pieces/I_Han_Horse.png").convert_alpha(),
		PieceType.CANNON: pygame.image.load("Pieces/I_Han_Cannon.png").convert_alpha(),
		PieceType.CHARIOT: pygame.image.load("Pieces/I_Han_Chariot.png").convert_alpha(),
		PieceType.PAWN: pygame.image.load("Pieces/I_Han_Pawn.png").convert_alpha()
	}

	# load International Cho-side piece images
	I_cho_piece_images = {
		PieceType.KING : pygame.image.load("Pieces/I_Cho_King.png").convert_alpha(),
		PieceType.ADVISOR : pygame.image.load("Pieces/I_Cho_Advisor.png").convert_alpha(),
		PieceType.ELEPHANT: pygame.image.load("Pieces/I_Cho_Elephant.png").convert_alpha(),
		PieceType.HORSE: pygame.image.load("Pieces/I_Cho_Horse.png").convert_alpha(),
		PieceType.CANNON: pygame.image.load("Pieces/I_Cho_Cannon.png").convert_alpha(),
		PieceType.CHARIOT: pygame.image.load("Pieces/I_Cho_Chariot.png").convert_alpha(),
		PieceType.PAWN: pygame.image.load("Pieces/I_Cho_Pawn.png").convert_alpha()
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

	piece_display = {
		PieceType.KING: PreGamePieceDisplay.KING.value,
		PieceType.ADVISOR: PreGamePieceDisplay.ADVISOR.value,
		PieceType.ELEPHANT: PreGamePieceDisplay.ELEPHANT.value,
		PieceType.HORSE: PreGamePieceDisplay.HORSE.value,
		PieceType.CANNON: PreGamePieceDisplay.CANNON.value,
		PieceType.CHARIOT: PreGamePieceDisplay.CHARIOT.value,
		PieceType.PAWN: PreGamePieceDisplay.PAWN.value
	}
	
	# iterate through the player's pieces
	# and render the approiprotae piece by unpacking
	# the player.pieces into the following:
	# for PieceType in player's active pieces
	for janggi_piece in player.pieces:
		if player.color == "Han":
			if player.piece_convention == "International":
				piece_image = I_han_piece_images[janggi_piece.piece_type]
			else:
				piece_image = han_piece_images[janggi_piece.piece_type]
		else:
			if player.piece_convention == "International":
				piece_image = I_cho_piece_images[janggi_piece.piece_type]
			else:
				piece_image = cho_piece_images[janggi_piece.piece_type]
		piece_image = pygame.transform.scale(piece_image,
											 piece_sizes[janggi_piece.piece_type])
		# center the image correctly to its spot
		piece_image_pos = helper_funcs.reformat_piece(piece_display[janggi_piece.piece_type], piece_image)
		window.blit(piece_image, piece_image_pos)


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

	# load International Han-side piece images
	I_han_piece_images = {
		PieceType.KING: pygame.image.load("Pieces/I_Han_King.png").convert_alpha(),
		PieceType.ADVISOR: pygame.image.load("Pieces/I_Han_Advisor.png").convert_alpha(),
		PieceType.ELEPHANT: pygame.image.load("Pieces/I_Han_Elephant.png").convert_alpha(),
		PieceType.HORSE: pygame.image.load("Pieces/I_Han_Horse.png").convert_alpha(),
		PieceType.CANNON: pygame.image.load("Pieces/I_Han_Cannon.png").convert_alpha(),
		PieceType.CHARIOT: pygame.image.load("Pieces/I_Han_Chariot.png").convert_alpha(),
		PieceType.PAWN: pygame.image.load("Pieces/I_Han_Pawn.png").convert_alpha()
	}

	# load International Cho-side piece images
	I_cho_piece_images = {
		PieceType.KING : pygame.image.load("Pieces/I_Cho_King.png").convert_alpha(),
		PieceType.ADVISOR : pygame.image.load("Pieces/I_Cho_Advisor.png").convert_alpha(),
		PieceType.ELEPHANT: pygame.image.load("Pieces/I_Cho_Elephant.png").convert_alpha(),
		PieceType.HORSE: pygame.image.load("Pieces/I_Cho_Horse.png").convert_alpha(),
		PieceType.CANNON: pygame.image.load("Pieces/I_Cho_Cannon.png").convert_alpha(),
		PieceType.CHARIOT: pygame.image.load("Pieces/I_Cho_Chariot.png").convert_alpha(),
		PieceType.PAWN: pygame.image.load("Pieces/I_Cho_Pawn.png").convert_alpha()
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
	# and render the approiprotae piece by unpacking
	# the opponent.pieces into the following:
	# for PieceType in opponent's active pieces
	for janggi_piece in opponent.pieces:
		if player.color == "Cho":
			if player.piece_convention == "International":
				piece_image = I_han_piece_images[janggi_piece.piece_type]
			else:
				piece_image = han_piece_images[janggi_piece.piece_type]
		else:
			if player.piece_convention == "International":
				piece_image = I_cho_piece_images[janggi_piece.piece_type]
			else:
				piece_image = cho_piece_images[janggi_piece.piece_type]
		piece_image = pygame.transform.scale(piece_image,
																				 piece_sizes[janggi_piece.piece_type])
		# center the image correctly to its spot
		piece_image_pos = helper_funcs.reformat_piece(janggi_piece.image_location, piece_image)
		window.blit(piece_image, piece_image_pos)

	# iterate through the player's remaining pieces
	# and render the approiprotae piece by unpacking
	# the player.pieces into the following:
	# for PieceType in player's active pieces
	for janggi_piece in player.pieces:
		if player.color == "Han":
			if player.piece_convention == "International":
				piece_image = I_han_piece_images[janggi_piece.piece_type]
			else:
				piece_image = han_piece_images[janggi_piece.piece_type]
		else:
			if player.piece_convention == "International":
				piece_image = I_cho_piece_images[janggi_piece.piece_type]
			else:
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
def render_possible_spots(player, opponent, board, window):
	# determine the type of piece being moved
	for janggi_piece in player.pieces:
		if janggi_piece.is_clicked:
			match janggi_piece.piece_type.value:
				case "King":
					render_king_possible_spots(janggi_piece, player, board, window)
	
				case "Advisor":
					render_advisor_possible_spots(janggi_piece, player,  board, window)
	
				case "Elephant":
					render_elephant_possible_spots(janggi_piece, player, opponent, board, window)
	
				case "Horse":
					render_horse_possible_spots(janggi_piece, player, opponent, board, window)
	
				case "Cannon":
					render_cannon_possible_spots(janggi_piece, player,opponent,  board, window)
	
				case "Chariot":
					render_chariot_possible_spots(janggi_piece, player, opponent,  board, window)
	
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
	# Possible moves for the piece based on current possition (L/R/U)
	# view board as vertical (standard) where top of board is beginning of
	# the 2D list
	# (-x, y) --> left x spots
	# (+x, y) --> right x spots
	# (x, -y) --> up y spots
	# (x, +y) --> down y spots
	#				( (UpLeft)   (Up)    (UpRight)
	# 				  (Left) 		     (Right) 
	# 				  (DownLeft) (Down)  (DownRight))
	full_moves = ((-1, -1),  (0, -1),  (1, -1),
				  (-1, 0),   		   (1, 0), 
				  (-1, 1),   (0, 1),   (1, 1), )
	
	orthogonal_moves = (	      (0, -1),	    
				   	    (-1, 0),		    (1,0),
								  (0, 1),		   )
	
	# piece can move diagonally if on any of these spots within the palace
	diagonal_spots = ((0, 0),	  		   (2, 0),
				   				 (1, 1),
				   	  (0, 2),			   (2, 2)  )

	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(board.cho_palace):
		for file, spot in enumerate(row):
			# find where piece is relative to board
			if spot == janggi_piece.location:
				# check if piece can move diagonally in palace
				if (rank, file) in diagonal_spots:
					possible_moves = full_moves
				# piece can only move orthogonally
				else:
					possible_moves = orthogonal_moves

				# update move coordinates for the piece where it can move
				for move in possible_moves:
					new_rank = rank + move[0]
					new_file = file + move[1]

					# check that move location is within board
					if ((0 <= new_rank < len(board.cho_palace))
							and (0 <= new_file < len(row))):
						# take the coords for the spot to potentially highlight
						new_rect = board.cho_palace_collisions[new_rank][new_file]
						
						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece):
							
							# potential jump-to spot found, align the rectangle for drawing
							# spot in board
							new_spot = board.cho_palace[new_rank][new_file]
							new_spot = helper_funcs.reformat_spot_collision(new_spot,
																			board.cho_palace_collisions[new_rank]
																			[new_file])
							
							# rectangle bounds for drawing the spot rectangle
							rectangle = (new_spot[0], new_spot[1], 
													 constants.spot_collision_size[0], 
													 constants.spot_collision_size[1])
							
							# render the possible spot
							pygame.draw.rect(window, constants.GREEN, rectangle)
	return

#-----------------------------------------------------------------------------------
# Function that will render the possible move spots on the board for advisor piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_advisor_possible_spots(janggi_piece, player, board, window):
	# Possible moves for the piece based on current possition (L/R/U)
	# view board as vertical (standard) where top of board is beginning of
	# the 2D list
	# (-x, y) --> left x spots
	# (+x, y) --> right x spots
	# (x, -y) --> up y spots
	# (x, +y) --> down y spots
	#				( (UpLeft)   (Up)    (UpRight)
	# 				  (Left) 		     (Right) 
	# 				  (DownLeft) (Down)  (DownRight))
	full_moves = ((-1, -1),  (0, -1),  (1, -1),
				  (-1, 0),   		   (1, 0), 
				  (-1, 1),   (0, 1),   (1, 1), )
	
	orthogonal_moves = (	      (0, -1),	    
				   	    (-1, 0),		    (1,0),
								  (0, 1),		   )
	
	# piece can move diagonally if on any of these spots within the palace
	diagonal_spots = ((0, 0),	  		   (2, 0),
				   				 (1, 1),
				   	  (0, 2),			   (2, 2)  )

	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(board.cho_palace):
		for file, spot in enumerate(row):
			# find where piece is relative to board
			if spot == janggi_piece.location:
				# check if piece can move diagonally in palace
				if (rank, file) in diagonal_spots:
					possible_moves = full_moves
				# piece can only move orthogonally
				else:
					possible_moves = orthogonal_moves

				# update move coordinates for the piece where it can move
				for move in possible_moves:
					new_rank = rank + move[0]
					new_file = file + move[1]

					# check that move location is within board
					if ((0 <= new_rank < len(board.cho_palace))
							and (0 <= new_file < len(row))):
						# take the coords for the spot to potentially highlight
						new_rect = board.cho_palace_collisions[new_rank][new_file]
						
						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece):
							
							# potential jump-to spot found, align the rectangle for drawing
							# spot in board
							new_spot = board.cho_palace[new_rank][new_file]
							new_spot = helper_funcs.reformat_spot_collision(new_spot,
																			board.cho_palace_collisions[new_rank]
																			[new_file])
							
							# rectangle bounds for drawing the spot rectangle
							rectangle = (new_spot[0], new_spot[1], 
													 constants.spot_collision_size[0], 
													 constants.spot_collision_size[1])
							
							# render the possible spot
							pygame.draw.rect(window, constants.GREEN, rectangle)
	return

#-----------------------------------------------------------------------------------
# Function that will render the possible move spots on the board for elephant piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_elephant_possible_spots(janggi_piece, player, opponent, board, window):
	def process_path(x): # Return orthogonal path position
		if x == 2 or x == -2:
			return 0
		elif x == 3:
			return 1
		else:
			return -1
	def process_diagonal_path(x): # Return diagonal path position
		if x == 2:
			return 1
		elif x == -2:
			return -1
		elif x == 3:
			return 2
		else:
			return -2

	# Possible moves for the piece based on current possition (L/R/U)
	# view board as vertical (standard) where top of board is beginning of
	# the 2D list
	# (-x, y) --> left x spots
	# (+x, y) --> right x spots
	# (x, -y) --> up y spots
	# (x, +y) --> down y spots
	#				[ (Left) , (Right), (Up)  ]
	possible_moves = [(-2, 3), (2, 3), (2, -3), (-2, -3), (3, -2), (3, 2), (-3, -2), (-3, 2)]
	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(board.coordinates):
		for file, spot in enumerate(row):
			# find where piece is relative to board
			if spot == janggi_piece.location:
				# Update move coordinates for the piece where it can move
				for move in possible_moves:
					new_rank = rank + move[0]
					new_file = file + move[1]
					path_rank = rank + process_path(move[0])
					path_file = file + process_path(move[1])
					diagonal_path_rank = rank + process_diagonal_path(move[0])
					diagonal_path_file = file + process_diagonal_path(move[1])

					# check that move location is in board
					if ((0 <= new_rank < len(board.coordinates))
							and (0 <= new_file < len(row))):
						# spot in board
						new_spot = board.coordinates[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = board.collisions[new_rank][new_file]
						# assemble the path to check
						path_to_check = [board.collisions[path_rank][path_file],board.collisions[diagonal_path_rank][diagonal_path_file]]
						
						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						# Check the path's orthogonal and diagonal positions for ANY pieces to prevent illegal movement
						if (not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check[0].colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)
						     and not any(path_to_check[0].colliderect(piece.collision_rect) 
													 for piece in opponent.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check[1].colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)
						     and not any(path_to_check[1].colliderect(piece.collision_rect) 
													 for piece in opponent.pieces 
													 if piece != janggi_piece)):
							# rectangle bounds for drawing the spot rectangle
							rectangle = (new_spot[0], new_spot[1], 
													 constants.spot_collision_size[0], 
													 constants.spot_collision_size[1])
							
							# render the possible spot
							pygame.draw.rect(window, constants.GREEN, rectangle)
	return

#-----------------------------------------------------------------------------------
# Function that will render the possible move spots on the board for the horse piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_horse_possible_spots(janggi_piece, player, opponent, board, window):
	def process_path(x): # Return orthogonal path position
		if x == 1 or x == -1:
			return 0
		elif x == 2:
			return 1
		else:
			return -1

	# Possible moves for the piece based on current possition (L/R/U)
	# view board as vertical (standard) where top of board is beginning of
	# the 2D list
	# (-x, y) --> left x spots
	# (+x, y) --> right x spots
	# (x, -y) --> up y spots
	# (x, +y) --> down y spots
	#				[ (Left) , (Right), (Up)  ]
	possible_moves = [(-1, 2), (1, 2), (1, -2), (-1, -2), (2, -1), (2, 1), (-2, -1), (-2, 1)]
	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(board.coordinates):
		for file, spot in enumerate(row):
			# find where piece is relative to board
			if spot == janggi_piece.location:
				# Update move coordinates for the piece where it can move
				for move in possible_moves:
					new_rank = rank + move[0]
					new_file = file + move[1]
					path_rank = rank + process_path(move[0])
					path_file = file + process_path(move[1])

					# check that move location is in board
					if ((0 <= new_rank < len(board.coordinates))
							and (0 <= new_file < len(row))):
						# spot in board
						new_spot = board.coordinates[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = board.collisions[new_rank][new_file]
						# note path to check
						path_to_check = board.collisions[path_rank][path_file]
						
						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						# Check the path's orthogonal position for ANY pieces to prevent illegal movement
						if (not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)
						     and not any(path_to_check.colliderect(piece.collision_rect) 
													 for piece in opponent.pieces 
													 if piece != janggi_piece)):
							# rectangle bounds for drawing the spot rectangle
							rectangle = (new_spot[0], new_spot[1], 
													 constants.spot_collision_size[0], 
													 constants.spot_collision_size[1])
							
							# render the possible spot
							pygame.draw.rect(window, constants.GREEN, rectangle)
	return

#-----------------------------------------------------------------------------------
# Function that will render possible move spots on the board for the cannon piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_cannon_possible_spots(janggi_piece, player, opponent, board, window):
	# implement logic here
	possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Get a list of all the pieces on the board
	all_pieces = player.pieces + opponent.pieces

    # Iterate over the board to find the current location of the cannon
	for rank, row in enumerate(board.coordinates):
		for file, spot in enumerate(row):
			if spot == janggi_piece.location:
				# Cannon found, now check possible movement directions
				for move in possible_moves:
					new_rank = rank + move[0]
					new_file = file + move[1]

                    # Continue moving along the path in the given direction until out of bounds
					while (0 <= new_rank < len(board.coordinates)) and (0 <= new_file < len(row)):
						piece_in_way = False

						for check_piece in all_pieces:
							# Check here if the piece is a cannon
							if (board.coordinates[new_rank][new_file] == check_piece.location) and not (check_piece.piece_type.value == "Cannon"):
								# A piece is in the way, cannon jumps over it
								piece_in_way = True
								break

						if piece_in_way:
							# Jump over the piece
							new_rank += move[0]
							new_file += move[1]

							# Check if after jumping the new position is out of bounds
							piece_in_way = False
							while ((0 <= new_rank < len(board.coordinates)) and (0 <= new_file < len(row)) and not piece_in_way):
								piece_in_way = False
								for check_piece in all_pieces:
									if (board.coordinates[new_rank][new_file] == check_piece.location) and not (check_piece.piece_type.value == "Cannon"):
										# A piece is in the way, cannon jumps over it
										piece_in_way = True
										break

								# If after first jump, nothing is there, then keep moving through the open space
								if not piece_in_way:
									new_spot = board.coordinates[new_rank][new_file]
									new_rect = board.collisions[new_rank][new_file]

									# Check if the spot is valid (not occupied by a player's piece, except for the cannon)
									if not any(new_rect.colliderect(piece.collision_rect) 
																for piece in player.pieces 
																if piece != janggi_piece):
										
										# rectangle bounds for drawing the spot rectangle
										rectangle = (new_spot[0], new_spot[1], 
																constants.spot_collision_size[0], 
																constants.spot_collision_size[1])
										
										# render the possible spot
										pygame.draw.rect(window, constants.GREEN, rectangle)

									# Keep moving
									new_rank += move[0]
									new_file += move[1]

								# There was a piece there, so stop.	
								else:
									break

							# Return back to move-in-possible-moves loop so it cant skip pieces
							break
						else:
							# Continue moving in the current direction if no piece is found
							new_rank += move[0]
							new_file += move[1]
	return

#-----------------------------------------------------------------------------------
# Function that will render possible move spots on the board for the chariot piece
# INPUT: Player object, Opponent Object, board object, pygame surface object
# OUTPUT: All possible jump-to spots will be highlighted
#-----------------------------------------------------------------------------------
def render_chariot_possible_spots(janggi_piece, player, opponent, board, window):
    # Define rook-like moves (up, down, left, right)
    rook_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Diagonal moves if inside the palace
    diagonal_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    # Combine all pieces from both players
    all_pieces = player.pieces + opponent.pieces

    # Iterate over the board to find the current location of the chariot
    for rank, row in enumerate(board.coordinates):
        for file, spot in enumerate(row):
            if spot == janggi_piece.location:
                # Chariot found, now set the movement directions
                possible_moves = rook_moves

                # If the chariot is in the palace, allow diagonal movement
                if helper_funcs.is_in_palace(rank, file):
                    possible_moves += diagonal_moves
                
                # Check movement in all possible directions
                for move in possible_moves:
                    new_rank = rank
                    new_file = file
                    
                    while True:
                        new_rank += move[0]
                        new_file += move[1]
                        
                        # Ensure the move is within the bounds of the board
                        if not (0 <= new_rank < len(board.coordinates) and 0 <= new_file < len(row)):
                            break  # Out of board bounds, stop in this direction

                        new_spot = board.coordinates[new_rank][new_file]
                        new_rect = board.collisions[new_rank][new_file]
                        
                        # Check if the new spot is occupied by any piece
                        if any(new_rect.colliderect(piece.collision_rect) for piece in all_pieces):
                            # If it collides with an opponent's piece, highlight for capture
                            if any(new_rect.colliderect(piece.collision_rect) 
                                   for piece in opponent.pieces):
                                # Rectangle bounds for drawing the capture move
                                rectangle = (new_spot[0], new_spot[1],
                                             constants.spot_collision_size[0], 
                                             constants.spot_collision_size[1])
                                
                                # Render the capture spot
                                pygame.draw.rect(window, constants.GREEN, rectangle)
                            break  # Stop if there's any piece blocking the way

                        # If the spot is valid for the player (not occupied by their own pieces)
                        if not any(new_rect.colliderect(piece.collision_rect) 
                                   for piece in player.pieces if piece != janggi_piece):
                            # Rectangle bounds for drawing the possible move
                            rectangle = (new_spot[0], new_spot[1],
                                         constants.spot_collision_size[0], 
                                         constants.spot_collision_size[1])
                            
                            # Render the possible move spot
                            pygame.draw.rect(window, constants.GREEN, rectangle)

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
	#				 ((Left),   (Up),  (Right))
	possible_moves = ((-1, 0), (0, -1), (1, 0))
	
	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(board.coordinates):
		for file, spot in enumerate(row):
			# find where piece is relative to board
			if spot == janggi_piece.location:
				# check if piece can also use palace diagonals, then render those as well
				if helper_funcs.can_use_palace_diagonals(janggi_piece, board):
					render_pawn_possible_palace_spots(player, window, janggi_piece, board)
				
				# Show where piece can move normaly by looking at each of 
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
# Function that will render the possible move spots on the board for the pawn piece
# given that the piece is inside the palace
# INPUT: Player object, pygame surface object, piece object, board object
# OUTPUT: All possible jump-to spots will be highlighted within the palace
#-----------------------------------------------------------------------------------
def render_pawn_possible_palace_spots(player, window, janggi_piece, board):
	#			   ((UpLeft),       (UpRight))
	palace_moves = ((-1, -1),		(1, -1))

	# if the pawn is in a palace diagonal , it can take palace moves
	if helper_funcs.can_use_palace_diagonals(janggi_piece, board):
		for rank, row in enumerate(board.han_palace):
			for file, spot in enumerate(row):
				# find the piece's location relative to palace
				if spot == janggi_piece.location:
					# look at each potential palace diagonal move
					for move in palace_moves:
						new_rank = rank + move[0]
						new_file = file + move[1]

						# check that move location is in palace
						if ((0 <= new_rank < len(board.han_palace))
								and (0 <= new_file < len(row))
								and (helper_funcs.is_inside_palace(board, new_rank, new_file))):
							# take the coords for the spot to potentially highlight
							new_rect = board.han_palace_collisions[new_rank][new_file]
										
							# Make sure spot is not occupied by another piece of the player
							# but exclude the piece being moved from being checked
							if not any(new_rect.colliderect(piece.collision_rect) 
														for piece in player.pieces 
														if piece != janggi_piece):
								# potential jump-to spot found, align the rectangle for drawing
								new_spot = board.han_palace[new_rank][new_file]
								new_spot = helper_funcs.reformat_spot_collision(new_spot,
																				board.han_palace_collisions[new_rank]
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