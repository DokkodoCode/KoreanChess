"""
----------------------helper_funcs.py-----------------------------
o This file is to hold any logical/helper functions to be 
	called by state.py
o Try to avoid any imports/constants in this file
o Last Modified - October 4th 2024
------------------------------------------------------------------
"""

import json

#-----------------------------------------------------------------------------------
# Function that will send player's board data to other player for synchronization
# INPUT: 
# OUTPUT: 
#-----------------------------------------------------------------------------------
def send_move_over_network(move_data):
	# Send the JSON data to the other user
	pass

#-----------------------------------------------------------------------------------
# Function that will receive board data from other player for synchronization
# INPUT: 
# OUTPUT: 
#-----------------------------------------------------------------------------------
def get_move_from_network(move_data, player, opponent, board):
	# Deserialize the JSON data
	try:
		move_info = json.loads(move_data)
	except json.JSONDecodeError:
		print("Received invalid move data")
		return

	piece_type = move_info.get("piece_type")
	image_location = move_info.get("image_location")
	collision_rect_topleft = move_info.get("collision_rect.topleft")
	from_pos = move_info.get("from")
	to_pos = move_info.get("to")

	# Validate and update the board
	if piece_type and image_location and from_pos and to_pos:
		from_rank, from_file = from_pos
		to_rank, to_file = to_pos

		# Find the piece that needs to be moved
		piece_to_move = next((p for p in opponent.pieces if p.piece_type.value == piece_type and p.location == (from_rank, from_file)), None)
		if piece_to_move:
			# Here you might want to add specific logic to validate the move
			# For example, check if the move is valid according to game rules
			# This would typically involve calling the same move functions you used earlier

			# Update the piece's location
			piece_to_move.location = (to_rank, to_file)
			# Update collision rectangle and image location if necessary
			piece_to_move.collision_rect.topleft = collision_rect_topleft
			piece_to_move.image_location = image_location
			# (this would depend on how you're managing piece graphics)

			# Update the piece's collision rectangle based on the new location
			# (Assuming you have a way to convert the location back to a collision rectangle)
			# update_collision_rect(piece_to_move, board)

			# You may also need to handle removing opponent pieces if they are captured
			print(f"Moved {piece_type} from {from_pos} to {to_pos}")
		else:
			print("Piece to move not found or move invalid.")
	else:
		print("Received incomplete move data.")
	pass


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
def attempt_move(player, opponent, board, mouse_pos):
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
						if not move_king(janggi_piece, board, mouse_pos, player, opponent):
							return False
					case "Advisor":
						if not move_advisor(janggi_piece, board, mouse_pos, player, opponent):
							return False
					case "Elephant":
						if not move_elephant(janggi_piece, board, player, opponent, mouse_pos):
							return False
					case "Horse":
						if not move_horse(janggi_piece, board, player, opponent, mouse_pos):
							return False
					case "Cannon":
						if not move_cannon(janggi_piece, board, mouse_pos, player, opponent):
							return False
					case "Chariot":
						if not move_chariot(janggi_piece, board, mouse_pos, player, opponent):
							return False
					case "Pawn":
						if not move_pawn(janggi_piece, board, mouse_pos, player, opponent):
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
				original_location = janggi_piece.location
				janggi_piece.location = board.coordinates[rank][file]
				
				# Send move details over the network
				move_data = {
					"piece_type": janggi_piece.piece_type.value,
					"collision_rect.topleft": janggi_piece.collision_rect.topleft,
					"image_location": janggi_piece.image_location,
					"from": (original_location[0], original_location[1]),
					"to": (rank, file)
				}
				#send_move_over_network(json.dumps(move_data))

				return True
				
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked king piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_king(janggi_piece, board, mouse_pos, player, opponent):
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
					
					# check that move location is in palace
					if ((0 <= new_rank < len(board.cho_palace))
							and (0 <= new_file < len(row))):
						# spot in board
						new_spot = board.cho_palace[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = board.cho_palace_collisions[new_rank][new_file]

						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if (new_rect.collidepoint(mouse_pos)
							 and not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)):
							# update piece location and collision for valid move
							janggi_piece.location = new_spot
							janggi_piece.collision_rect.topleft = new_spot

							# check if move resulted in a capture
							detect_capture(player, opponent, janggi_piece)

							# valid move was made
							return True
						
	# no valid move was made
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked advisor piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def	move_advisor(janggi_piece, board, mouse_pos, player, opponent):
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
				   	  (0, 2),			   (2, 2))
	

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
					
					# check that move location is in palace
					if ((0 <= new_rank < len(board.cho_palace))
							and (0 <= new_file < len(row))):
						# spot in board
						new_spot = board.cho_palace[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = board.cho_palace_collisions[new_rank][new_file]

						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if (new_rect.collidepoint(mouse_pos)
							 and not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)):
							# update piece location and collision for valid move
							janggi_piece.location = new_spot
							janggi_piece.collision_rect.topleft = new_spot

							# check if move resulted in a capture
							detect_capture(player, opponent, janggi_piece)

							# valid move was made
							return True
						
	# no valid move was made
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked elephant piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_elephant(janggi_piece, board, player, opponent, mouse_pos):
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
						if (new_rect.collidepoint(mouse_pos)
							 and not any(new_rect.colliderect(piece.collision_rect) 
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
							# update piece location and collision for valid move
							janggi_piece.location = new_spot
							janggi_piece.collision_rect.topleft = new_spot
							# capture
							detect_capture(player, opponent, janggi_piece)
							return True
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked horse piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_horse(janggi_piece, board, player, opponent, mouse_pos):
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
						if (new_rect.collidepoint(mouse_pos)
							 and not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check.colliderect(piece.collision_rect) 
													 for piece in opponent.pieces 
													 if piece != janggi_piece)):
							# update piece location and collision for valid move
							janggi_piece.location = new_spot
							janggi_piece.collision_rect.topleft = new_spot
							# capture
							detect_capture(player, opponent, janggi_piece)
							return True
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked cannon piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_cannon(janggi_piece, board, mouse_pos, player, opponent):
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
									if (board.coordinates[new_rank][new_file] == check_piece.location):
										# A piece is in the way, cannon jumps over it
										piece_in_way = True
										break

								# If after first jump, nothing is there, then keep moving through the open space
								if not piece_in_way:
									new_spot = board.coordinates[new_rank][new_file]
									new_rect = board.collisions[new_rank][new_file]

									# Check if the spot is valid (not occupied by a player's piece, except for the cannon)
									if not any(new_rect.colliderect(piece.collision_rect) for piece in player.pieces if piece != janggi_piece):
										if not any(new_rect.collidepoint(mouse_pos) 
																	for piece in player.pieces 
																	if piece != janggi_piece):
										
											janggi_piece.location = new_spot
											janggi_piece.collision_rect.topleft = new_spot

											return True

									# Keep moving
									new_rank += move[0]
									new_file += move[1]

								# There was a piece there, so try to capture it.	
								else:
									new_spot = board.coordinates[new_rank][new_file]
									new_rect = board.collisions[new_rank][new_file]

									for check_piece in all_pieces:
										if ((not any(new_rect.colliderect(piece.collision_rect) for piece in player.pieces if piece != janggi_piece)) 
																				and (check_piece.piece_type.value != "Cannon")
																				and (board.coordinates[new_rank][new_file] == check_piece.location)):
											if new_rect.collidepoint(mouse_pos):
												janggi_piece.location = new_spot
												janggi_piece.collision_rect.topleft = new_spot

												# Check for capture
												

											return True
									break
								break

							# Return back to move-in-possible-moves loop so it cant skip pieces
							break
						else:
							# Continue moving in the current direction if no piece is found
							new_rank += move[0]
							new_file += move[1]
							break
	return False


	
#-----------------------------------------------------------------------------------
# Function that will move a clicked chariot piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_chariot(janggi_piece, board, mouse_pos, player, opponent):
	# Define rook-like moves for chariot (up, down, left, right)
	rook_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
	diagonal_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

	# Get the current location of the piece
	for rank, row in enumerate(board.coordinates):
		for file, spot in enumerate(row):
			# Find where the chariot is on the board
			if spot == janggi_piece.location:
				# Set initial possible moves (up, down, left, right)
				possible_moves = rook_moves
				
				# Check if the chariot is in the palace (to allow diagonal moves)
				if is_in_palace(rank, file):
					possible_moves += diagonal_moves
				
				# Check each possible direction for continuous movement
				for move in possible_moves:
					new_rank = rank
					new_file = file

					# Continue moving in the current direction until you hit a boundary or another piece
					while True:
						new_rank += move[0]
						new_file += move[1]

						# Ensure the move is within the bounds of the board
						if 0 <= new_rank < len(board.coordinates) and 0 <= new_file < len(row):
							# If moving diagonally, ensure that the move stays inside the palace
							if move in diagonal_moves and not is_in_palace(new_rank, new_file):
								break  # Stop diagonal movement if it exits the palace

							new_spot = board.coordinates[new_rank][new_file]
							new_rect = board.collisions[new_rank][new_file]
							
							# Check if the spot is occupied by a piece from the same player
							if any(new_rect.colliderect(piece.collision_rect) 
								   for piece in player.pieces if piece != janggi_piece):
								break  # Stop if there's a piece blocking the way
							
							# Check if this is the destination (the spot clicked by the mouse)
							if new_rect.collidepoint(mouse_pos):
								# Update the chariot's location and collision rect
								janggi_piece.location = new_spot
								janggi_piece.collision_rect.topleft = new_spot

								# Check for capture
								detect_capture(player, opponent, janggi_piece)

								return True

							# Stop if there's an opponent's piece (can move here but not beyond)
							if any(new_rect.colliderect(piece.collision_rect) 
								   for piece in opponent.pieces):
								break
						else:
							break  # Out of board bounds, stop in this direction
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked pawn piece to a valid location
# INPUT: piece object, board object, mouse position on window
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_pawn(janggi_piece, board, mouse_pos, player, opponent):
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
				
				# if the pawn is in a palace, it can take palace moves
				if can_use_palace_diagonals(janggi_piece, board):
					if move_pawn_palace(player, opponent, janggi_piece, board, mouse_pos):
						# valid palace move was made
						return True
					
				# normal moves (outside of palace diagonals)
				# update move coordinates for the piece where it can move
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

							# Make sure spot is not occupied by another piece of the player
							# but exclude the piece being moved from being checked
							if (new_rect.collidepoint(mouse_pos)
								and not any(new_rect.colliderect(piece.collision_rect) 
														for piece in player.pieces 
														if piece != janggi_piece)):
								# update piece location and collision for valid move
								janggi_piece.location = new_spot
								janggi_piece.collision_rect.topleft = new_spot

								# check if move resulted in a capture
								detect_capture(player, opponent, janggi_piece)

								# valid move made
								return True
							
	# no valid move made
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked pawn piece to a valid location given it can make
# a move diagonally within palace
# INPUT: player object, opponent object, piece object, board object, mouse position
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_pawn_palace(player, opponent, janggi_piece, board, mouse_pos):
	#			   ((UpLeft),       (UpRight))
	palace_moves = ((-1, -1),		(1, -1))

	# find piece location relative to palace
	for rank, row in enumerate(board.han_palace):
		for file, spot in enumerate(row):
			if spot == janggi_piece.location:
				# verify the palace diagonal piece can make
				for move in palace_moves:
					new_rank = rank + move[0]
					new_file = file + move[1]

					# check that move location is in board
					if ((0 <= new_rank < len(board.han_palace))
						and (0 <= new_file < len(row))
						and (is_inside_palace(board, new_rank, new_file))):
						# spot in palace
						new_spot = board.han_palace[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = board.han_palace_collisions[new_rank][new_file]
									
						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if (new_rect.collidepoint(mouse_pos)
							and not any(new_rect.colliderect(piece.collision_rect) 
										for piece in player.pieces 
										if piece != janggi_piece)):
							# update piece location and collision for valid move
							print(f"NS: {new_spot}")
							janggi_piece.location = new_spot
							janggi_piece.collision_rect.topleft = new_spot

							# check if move resulted in a capture
							detect_capture(player, opponent, janggi_piece)

							# valid move was made		
							return True
						
	# no valid move was made
	return False

#-----------------------------------------------------------------------------------
# Function that will determine if a move resides within the palace boundaries
# INPUT: board object, x coord of move, y coord of move
# OUTPUT: Boolean returned of whther move resides in a palace
#-----------------------------------------------------------------------------------
def is_inside_palace(board, new_rank, new_file):
	# han palace
	for rank, row in enumerate(board.han_palace):
		for file, spot in enumerate(row):
			if (new_rank, new_file) == (rank, file):
				return True 
			
	# cho palace
	for rank, row in enumerate(board.cho_palace):
		for file, spot in enumerate(row):
			if (new_rank, new_file) == (rank, file):
				return True
			
	# outside of palace		
	return False

#-----------------------------------------------------------------------------------
# Function that will determine if the piece is in the diagonal spots of the palace,
# meaning that the piece can now move diagonally along the palace in given spots 
# INPUT: Piece object being moved, board object
# OUTPUT: Boolean representing spot check result for that piece
#-----------------------------------------------------------------------------------		
def can_use_palace_diagonals(piece, board):
	# cho palace diagonals
	cho_diagonal_move_spots = (
								board.cho_palace[0][0],			board.cho_palace[0][2],

												board.cho_palace[1][1],

								board.cho_palace[2][0], 			board.cho_palace[2][2]
							  )

	# han palace diagonals
	han_diagonal_move_spots = (
								board.han_palace[0][0],			board.han_palace[0][2],

												board.han_palace[1][1],
												
								board.han_palace[2][0], 			board.han_palace[2][2]
							  )

	# determine if piece is in a diagonal spot in either palace
	for spot in cho_diagonal_move_spots:
		if spot == piece.location:
			return True
			
	for spot in han_diagonal_move_spots:
		if spot == piece.location:
			return True
	
	# piece not in a palace diagonal
	return False

#-----------------------------------------------------------------------------------
# Function that will determine if the passed in coordinates are within the palace
# INPUT: rank coordinate, file coordinate of piece
# OUTPUT: Boolean representing bounds check result
#-----------------------------------------------------------------------------------		
def is_in_palace(rank, file):
	# Return rank and file boundaries for if we are in palace coordiantes
	return ((7 <= file <= 9 and 3 <= rank <= 5) or  # Cho's palace
				(0 <= file <= 2 and 3 <= rank <= 5))    # Han's palace

#-----------------------------------------------------------------------------------
# Function that will check if capture occurs. This occurs when a piece is moved onto
# the opponent's piece and visa versa
# INPUT: Player object, Opponent object, piece that was moved
# OUTPUT: Boolean value returned, True if Bikjang, False if not
#-----------------------------------------------------------------------------------
def detect_capture(player, opponent, piece):
	# detect if player captured a piece if they moved piece
	if player.is_turn:
		for janggi_piece in opponent.pieces:
			if piece.collision_rect.colliderect(janggi_piece.collision_rect):
				print(f"Player's {piece.piece_type.value} captured Opponent's {janggi_piece.piece_type.value}")
				opponent.pieces.remove(janggi_piece)

	# detect if opponent captured a piece if they moved piece
	else:
		for janggi_piece in player.pieces:
			print("opponent captures")
			if piece.collision_rect.colliderect(janggi_piece.collision_rect):
				print(f"Opponent's {piece.piece_type.value} captured Player's {janggi_piece.piece_type.value}")
				player.pieces.remove(janggi_piece)

	return
#-----------------------------------------------------------------------------------
# Function that will check if Bikjang occurs. This occurs when the two King pieces
# are facing each other in the same row with no pieces in the way
# INPUT: Player object, Opponent object
# OUTPUT: Boolean value returned, True if Bikjang, False if not
#-----------------------------------------------------------------------------------
def detect_bikjang(player, opponent):
	player_king_location = None
	opponent_king_location = None

	# find player's king
	for janggi_piece in player.pieces:
		if janggi_piece.piece_type == "King":
			player_king_location = janggi_piece.location

	# find opponent's king
	for janggi_piece in opponent.pieces:
		if janggi_piece.piece_type == "King":
			opponent_king_location = janggi_piece.location

	# search for any blocking pieces between kings
	for janggi_piece in player.pieces + opponent.pieces:
		if (player_king_location 
	  		and opponent_king_location
	  		and janggi_piece.location[0] == player_king_location[0] 
	  		and opponent_king_location[1] < janggi_piece.location < player_king_location[1]):
			return False
		
	# kings are facing each other, bikjang ON
	return True

#-----------------------------------------------------------------------------------
#(WIP TODO)
# Function that will check if a piece moved cause a check state
# INPUT: Player object, opponent object, piece that was moved
# OUTPUT: Boolean returned for check state
#-----------------------------------------------------------------------------------
def detect_check(player, opponent, piece):

	if player.is_turn:
		# find opponent's king
		for janggi_piece in opponent.pieces:
			if janggi_piece.piece_type == "King":
				opponent_king_location = janggi_piece.location

	else:
		# find player's king
		for janggi_piece in player.pieces:
			if janggi_piece.piece_type == "King":
				player_king_location = janggi_piece.location

	return

#-----------------------------------------------------------------------------------
# Function that will update the player's chosen settings to form a pre-game template
# INPUT: Player object
# OUTPUT: a text file is created or up to date with the player's latest settings
#-----------------------------------------------------------------------------------
def update_player_settings(player):
	settings_file = "Settings/settings.txt"

	# these are the settings that will be written to file
	setting_options = [player.color, player.piece_convention, player.ai_level]

	# write the new file if not found
	try:
		with open(settings_file, 'x') as outfile:
			settings = '|'.join(setting_options)
			outfile.write(settings)

	# file already is present, write over it, updating the new settings
	except:
		FileExistsError
		print("Player's settings file already exists, updating player's settings...")
		with open(settings_file, 'w') as outfile:
			settings = '|'.join(setting_options)
			outfile.write(settings)