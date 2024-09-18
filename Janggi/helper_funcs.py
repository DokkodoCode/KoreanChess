"""
----------------------helper_funcs.py-----------------------------
o This file is to hold any logical/helper functions to be 
	called by state.py
o Try to avoid any imports/constants in this file
o Last Modified - September 17th 2024
------------------------------------------------------------------
"""

#-----------------------------------------------------------------------------------
# Function that will center the piece image in its spot on the board
# INPUT: coordinate of the piece object, image path asssociated with the object
# OUTPUT: Newly centered coordinates
#-----------------------------------------------------------------------------------
def reformat_piece(coordinate, piece_image):
	center_x = coordinate[0] + 37 - piece_image.get_width() // 2
	center_y = coordinate[1] + 37 - piece_image.get_height() // 2
	return center_x, center_y

#-----------------------------------------------------------------------------------
# Function that will center the piece collision rect in its spot on the board
# INPUT: coordinate of the piece object, rect object asssociated with the piece
# OUTPUT: Newly centered rectangle
#-----------------------------------------------------------------------------------
def reformat_piece_collision(coordinate, collision_rect):
	center_x = coordinate[0] + 37 - collision_rect.width // 2
	center_y = coordinate[1] + 37 - collision_rect.height // 2
	collision_rect.topleft = (center_x, center_y)
	return collision_rect

#-----------------------------------------------------------------------------------
# Function that will center collision rect of a spot on the board
# INPUT: coordinate of the spot in board, rect object asssociated with the spot
# OUTPUT: Newly centered spot rectangle
#-----------------------------------------------------------------------------------
def reformat_spot_collision(coordinate, collision_rect):
	center_x = coordinate[0] + 37 - collision_rect.width // 2
	center_y = coordinate[1] + 37 - collision_rect.height // 2
	collision_rect.topleft = (center_x, center_y)
	return collision_rect

#-----------------------------------------------------------------------------------
# Function that will check if the player has clicked one of their pieces
# INPUT: player object, mouse position on window
# OUTPUT: flags set if a valid piece clicked
#-----------------------------------------------------------------------------------
def player_piece_clicked(player, mouse_pos):
	# check all player's active pieces to see if any were clicked
	for piece in player.pieces:
		if piece.collision_rect.collidepoint(mouse_pos):
			piece.is_clicked = True # flag piece being moved
			player.is_clicked = True # flag player as attempting to move a piece
			return True
	return False

#-----------------------------------------------------------------------------------
# Function that will unclick the player's currently clicked piece when called 
# INPUT: player object
# OUTPUT: flags reset for clicked piece
#-----------------------------------------------------------------------------------
def player_piece_unclick(player):
	# check all player's active pieces to find clicked piece
	for piece in player.pieces:
		if piece.is_clicked:
			piece.is_clicked = False # flag piece being not moved
			player.is_clicked = False # flag player as no longer atempting to move piece

#-----------------------------------------------------------------------------------
# Function that will move a clicked piece to a valid location
# INPUT: player object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot, or nothing if not valid location
#-----------------------------------------------------------------------------------
def attempt_move(player, board, mouse_pos):
	# null piece for assigning
	janggi_piece = None
	# check all player's active pieces to see if any were clicked
	for piece in player.pieces:
		# return false if player tried to move onto their own piece
		if piece.collision_rect.collidepoint(mouse_pos):
			return False
		# assign the null piece otherwise
		elif piece.is_clicked:
			janggi_piece = piece

	# no clicked piece was found
	if janggi_piece is None:
		return False

	# check board collision rectangles for players move choice based on mouse position
	for rank, row in enumerate(board.collisions):
		for file, collision in enumerate(row):
			if janggi_piece is not None and collision.collidepoint(mouse_pos):	
				# check which piece it is
				match janggi_piece.piece_type.value:
					case "King":
						if not move_king(janggi_piece, board, mouse_pos):
							return False
					case "Advisor":
						if not move_advisor(janggi_piece, board, mouse_pos):
							return False
					case "Elephant":
						if not move_elephant(janggi_piece, board, mouse_pos):
							return False
					case "Horse":
						if not move_horse(janggi_piece, board, mouse_pos):
							return False
					case "Cannon":
						if not move_cannon(janggi_piece, board, mouse_pos):
							return False
					case "Chariot":
						if not move_chariot(janggi_piece, board, mouse_pos):
							return False
					case "Pawn":
						if not move_pawn(janggi_piece, player, board, mouse_pos):
							return False
					case _:
						raise ValueError("Invalid piece type")
					
				# We need to account for the three different pieces
				# having three different sizes rect objects can use 
				# .size to get the size of the collision rectangle
				janggi_piece_size = janggi_piece.collision_rect.size
				center_x = collision[0] + (collision.width // 2) - (janggi_piece_size[0] // 2)
				center_y = collision[1] + (collision.height // 2) - (janggi_piece_size[1] // 2)
	
				# update the moved piece's collision rectangle
				janggi_piece.collision_rect.topleft = (center_x, center_y)
				
				# move piece's image and associated piece to new spot
				center_x = collision[0] + 22 - collision.width // 2
				center_y = collision[1] + 22 - collision.height // 2
				janggi_piece.image_location = (center_x, center_y)
				janggi_piece.location = board.coordinates[rank][file]
				
				return True
				
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked king piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_king(janggi_piece, board, mouse_pos):
	# implement piece logic here
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked advisor piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def	move_advisor(janggi_piece, board, mouse_pos):
	# implement piece logic here
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked elephant piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_elephant(janggi_piece, board, mouse_pos):
	# implement piece logic here
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked horse piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_horse(janggi_piece, board, mouse_pos):
	# implement piece logic here
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked cannon piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_cannon(janggi_piece, board, mouse_pos):
	# implement piece logic here
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked chariot piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_chariot(janggi_piece, board, mouse_pos):
	# implement piece logic here
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked pawn piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_pawn(janggi_piece, player, board, mouse_pos):
	# possible moves for the piece based on current possition (L/R/U)
	possible_moves = [(-1, 0), (1, 0), (0, -1)]
	
	# check each spot in the board for valid locations
	for rank, row in enumerate(board.coordinates):
		for file, spot in enumerate(row):
			# find where piece is relative to board
			if spot == janggi_piece.location:
				# Update coordinates to show the board collision rectangles 
				# of where the piece can move
				for move in possible_moves:
					new_rank = rank + move[0]
					new_file = file + move[1]

					# check that move location is in board
					if ((0 <= new_rank < len(board.coordinates))
							and (0 <= new_file < len(row))):
						# spot in board
						new_spot = board.coordinates[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = board.collisions[new_rank][new_file]
						
						# now make sure move is not onto another piece owned by player
						if (new_rect.collidepoint(mouse_pos)
							 and not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)):
							# update piece location and collision if valid move
							janggi_piece.location = new_spot
							janggi_piece.collision_rect.topleft = new_spot
							return True
	return False
							