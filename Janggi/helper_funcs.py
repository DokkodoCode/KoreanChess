"""
----------------------helper_funcs.py-----------------------------
o This file is to hold any logical/helper functions to be 
	called by state.py
o Last Modified - November 11th 2024
------------------------------------------------------------------
"""
import json
import pygame
import random

# local file imports, see individ file for details
import constants

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

def read_move(str):
	str = str.split(",")
	return int(str[0]), int(str[1])

def make_move(tup):
	return str(tup[0] + "," + tup[1])


#-----------------------------------------------------------------------------------
# Function that will center the piece image in its spot on the board
# INPUT: coordinate of the piece object, image path asssociated with the object
# OUTPUT: Newly centered coordinates
#-----------------------------------------------------------------------------------
def reformat_piece(coordinate, piece_image):
	# 32 32
	center_x = coordinate[0] + 32 - piece_image.get_width() // 2
	center_y = coordinate[1] + 32 - piece_image.get_height() // 2
	return center_x, center_y

#-----------------------------------------------------------------------------------
# Function that will center the piece collision rect in its spot on the board
# INPUT: coordinate of the piece object, rect object asssociated with the piece
# OUTPUT: Newly centered rectangle
#-----------------------------------------------------------------------------------
def reformat_piece_collision(coordinate, collision_rect):
	center_x = coordinate[0] + 32 - collision_rect.width // 2
	center_y = coordinate[1] + 32 - collision_rect.height // 2
	collision_rect.topleft = (center_x, center_y)
	return collision_rect

#-----------------------------------------------------------------------------------
# Function that will center collision rect of a spot on the board
# INPUT: coordinate of the spot in board, rect object asssociated with the spot
# OUTPUT: Newly centered spot rectangle
#-----------------------------------------------------------------------------------
def reformat_spot_collision(coordinate, collision_rect):
	center_x = coordinate[0] + 32 - collision_rect.width // 2
	center_y = coordinate[1] + 32 - collision_rect.height // 2
	collision_rect.topleft = (center_x, center_y)
	return collision_rect

#-----------------------------------------------------------------------------------
# Function that will assign the AI a random horse lineup
# INPUT: AI player, board
# OUTPUT: starting line-up positions for AI updated
#-----------------------------------------------------------------------------------
def choose_ai_lineup(ai_player):
	# Right horse and or left horse may swap w/ associated chariot/elephant
	# right-side horse <-> right-side elephant | left-side horse <-> left-side elephant
	# left-side horse <-> left-side chariot | left-side horse <-> left-side elephant
	# 0 = no swap, 1 = swap
	swap = random.randint(0, 1)
	if swap == 0:
		return
	# 0 = left-side, 1 = right-side, 2 = both
	else:
		side = random.randint(0,2)
		if side == 0:
			# swap left horse with left elephant
			swap_pieces(ai_player.pieces[5], ai_player.pieces[3])
		elif side == 1:
			# swap right horse with right elephant
			swap_pieces(ai_player.pieces[6], ai_player.pieces[4])
		else:
			# swap left horse with left elephant
			swap_pieces(ai_player.pieces[5], ai_player.pieces[3])
			# swap right horse with right elephant
			swap_pieces(ai_player.pieces[6], ai_player.pieces[4])

#-----------------------------------------------------------------------------------
# Function that will swap two pieces locations on the board
# INPUT: piece1, piece2
# OUTPUT: piece locations swapped
#-----------------------------------------------------------------------------------
def swap_pieces(piece1, piece2):
	# swap the two piece locations
	temp = piece1.location
	piece1.location = piece2.location
	piece2.location = temp

	# and swap the two piece collision rectangles
	temp = piece1.collision_rect.topleft
	piece1.collision_rect.topleft = piece2.collision_rect.topleft
	piece2.collision_rect.topleft = temp

	# then swap the two piece image locations
	temp = piece1.image_location
	piece1.image_location = piece2.image_location
	piece2.image_location = temp

#-----------------------------------------------------------------------------------
# Function that will check if the player has clicked one of their pieces
# INPUT: player whose turn it is, mouse position on window
# OUTPUT: flags set if a valid piece clicked
#-----------------------------------------------------------------------------------
def player_piece_clicked(active_player, mouse_pos):
	# check all player's active pieces to see if any were clicked
	for piece in active_player.pieces:
		if piece.collision_rect.collidepoint(mouse_pos):
			piece.is_clicked = True # flag piece being moved
			active_player.is_clicked = True # flag player as attempting to move a piece
			return True
	return False

#-----------------------------------------------------------------------------------
# Function that will unclick the player's currently clicked piece when called 
# INPUT: player whose turn it is
# OUTPUT: flags reset for clicked piece
#-----------------------------------------------------------------------------------
def player_piece_unclick(active_player):
	# check all player's active pieces to find clicked piece
	for piece in active_player.pieces:
		if piece.is_clicked:
			piece.is_clicked = False # flag piece being not moved
			active_player.is_clicked = False # flag player as no longer atempting to move piece

#-----------------------------------------------------------------------------------
# Function that will move a clicked piece to a valid location
# INPUT: player, waiting player, board, mouse position on window, any game condition
# OUTPUT: Piece is remapped to valid spot, or nothing if not valid location
#-----------------------------------------------------------------------------------
def attempt_move(active_player, waiting_player, board, mouse_pos, condition):
	# null piece for assigning
	janggi_piece = None
	# check all player's active pieces to see if any were clicked
	for piece in active_player.pieces:
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
						if not move_king(janggi_piece, board, mouse_pos, active_player, waiting_player, condition):
							return False
					case "Advisor":
						if not move_advisor(janggi_piece, board, mouse_pos, active_player, waiting_player, condition):
							return False
					case "Elephant":
						if not move_elephant(janggi_piece, board, active_player, waiting_player, mouse_pos, condition):
							return False
					case "Horse":
						if not move_horse(janggi_piece, board, active_player, waiting_player, mouse_pos, condition):
							return False
					case "Cannon":
						if not move_cannon(janggi_piece, board, mouse_pos, active_player, waiting_player, condition):
							return False
					case "Chariot":
						if not move_chariot(janggi_piece, board, mouse_pos, active_player, waiting_player, condition):
							return False
					case "Pawn":
						if not move_pawn(janggi_piece, board, mouse_pos, active_player, waiting_player, condition):
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
				janggi_piece.image_location = board.coordinates[rank][file]
				
				original_location = janggi_piece.location
				#janggi_piece.location = board.coordinates[rank][file]
				
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
# INPUT: piece, board, mouse position on window, player, waiting player, game cond
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_king(janggi_piece, board, mouse_pos, active_player, waiting_player, condition="None"):
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
	full_moves = [(-1, -1),  (0, -1),  (1, -1),
				  (-1, 0),   		   (1, 0), 
				  (-1, 1),   (0, 1),   (1, 1) ]
	
	orthogonal_moves = [	      (0, -1),	    
				   		(-1, 0),		    (1,0),
								  (0, 1)		   ]
	
	# piece can move diagonally if on any of these spots within the palace
	diagonal_spots = [(0, 0),	  		   (2, 0),
				   				 (1, 1),
				   	  (0, 2),			   (2, 2)  ]
	
	# during bikjang, the King cannot move orthoganally up or down
	if condition == "Bikjang":
		full_moves.remove((0, -1))
		full_moves.remove((0, 1))
		orthogonal_moves.remove((0, -1))
		orthogonal_moves.remove((0, 1))

	# define which palace to use based on active player's perspective
	if active_player.board_perspective == "Bottom":
		palace = board.bottom_palace
		palace_collisions = board.bottom_palace_collisions
	else:
		palace = board.top_palace
		palace_collisions = board.top_palace_collisions

	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(palace):
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
					if ((0 <= new_rank < len(palace))
							and (0 <= new_file < len(row))):
						# spot in board
						new_spot = palace[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = palace_collisions[new_rank][new_file]

						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if (new_rect.collidepoint(mouse_pos)
							 and not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in active_player.pieces 
													 if piece != janggi_piece)):
							
							# consider move limitations based on conditions
							if (condition == "None" or
								condition == "Bikjang" and move_can_break_bikjang(active_player, waiting_player, janggi_piece, new_spot) or
								condition == "Check" and move_can_break_check(active_player, waiting_player, board, janggi_piece, new_spot)):
									# update piece location and collision for valid move
									temp = janggi_piece.location
									temp_rect = janggi_piece.collision_rect.topleft

									janggi_piece.location = new_spot
									janggi_piece.collision_rect.topleft = new_spot

									# make sure move does not leave own king vulnerable, cancel move if it does
									if (detect_check(active_player, waiting_player, board) and 
										find_piece_causing_check(active_player, waiting_player, board).location != janggi_piece.location):
										janggi_piece.location = temp
										janggi_piece.collision_rect.topleft = temp_rect
										
									# valid move was made
									else:
										# now check if the valid move resulted in a capture
										if detect_capture(waiting_player, janggi_piece):
											capture_piece(waiting_player, janggi_piece)

										# valid move was made
										return True
						
	# no valid move was made
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked advisor piece to a valid location
# INPUT: piece, board, mouse position on window, player, waiting player, game cond
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def	move_advisor(janggi_piece, board, mouse_pos, active_player, waiting_player, condition="None"):
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
	
	# define which palace to use based on active player's perspective
	if active_player.board_perspective == "Bottom":
		palace = board.bottom_palace
		palace_collisions = board.bottom_palace_collisions
	else:
		palace = board.top_palace
		palace_collisions = board.top_palace_collisions

	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(palace):
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
					if ((0 <= new_rank < len(palace))
							and (0 <= new_file < len(row))):
						# spot in board
						new_spot = palace[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = palace_collisions[new_rank][new_file]

						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if (new_rect.collidepoint(mouse_pos)
							 and not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in active_player.pieces 
													 if piece != janggi_piece)):
							
							# consider move limitations based on conditions
							if (condition == "None" or
								condition == "Bikjang" and move_can_break_bikjang(active_player, waiting_player, janggi_piece, new_spot) or
								condition == "Check" and move_can_break_check(active_player, waiting_player, board, janggi_piece, new_spot)):
									# update piece location and collision for valid move
									temp = janggi_piece.location
									temp_rect = janggi_piece.collision_rect.topleft

									janggi_piece.location = new_spot
									janggi_piece.collision_rect.topleft = new_spot

									# make sure move does not leave own king vulnerable, cancel move if it does
									if (detect_check(active_player, waiting_player, board) and 
										find_piece_causing_check(active_player, waiting_player, board).location != janggi_piece.location):
										janggi_piece.location = temp
										janggi_piece.collision_rect.topleft = temp_rect
										
									# valid move was made
									else:
										# now check if the valid move resulted in a capture
										if detect_capture(waiting_player, janggi_piece):
											capture_piece(waiting_player, janggi_piece)

										# valid move was made
										return True
						
	# no valid move was made
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked elephant piece to a valid location
# INPUT: piece, board, mouse position on window, player, waiting player, game cond
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_elephant(janggi_piece, board, active_player, waiting_player, mouse_pos, condition="None"):
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
													 for piece in active_player.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check[0].colliderect(piece.collision_rect) 
													 for piece in active_player.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check[0].colliderect(piece.collision_rect) 
													 for piece in waiting_player.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check[1].colliderect(piece.collision_rect) 
													 for piece in active_player.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check[1].colliderect(piece.collision_rect) 
													 for piece in waiting_player.pieces 
													 if piece != janggi_piece)):
							
							# consider move limitations based on conditions
							if (condition == "None" or
								condition == "Bikjang" and move_can_break_bikjang(active_player, waiting_player, janggi_piece, new_spot) or
								condition == "Check" and move_can_break_check(active_player, waiting_player, board, janggi_piece, new_spot)):
									# update piece location and collision for valid move
									temp = janggi_piece.location
									temp_rect = janggi_piece.collision_rect.topleft

									janggi_piece.location = new_spot
									janggi_piece.collision_rect.topleft = new_spot

									# make sure move does not leave own king vulnerable, cancel move if it does
									if (detect_check(active_player, waiting_player, board) and 
										find_piece_causing_check(active_player, waiting_player, board).location != janggi_piece.location):
										janggi_piece.location = temp
										janggi_piece.collision_rect.topleft = temp_rect
										
									# valid move was made
									else:
										# now check if the valid move resulted in a capture
										if detect_capture(waiting_player, janggi_piece):
											capture_piece(waiting_player, janggi_piece)

										# valid move was made
										return True
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked horse piece to a valid location
# INPUT: piece, board, mouse position on window, player, waiting player, game cond
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_horse(janggi_piece, board, active_player, waiting_player, mouse_pos, condition="None"):
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
													 for piece in active_player.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check.colliderect(piece.collision_rect) 
													 for piece in active_player.pieces 
													 if piece != janggi_piece)
							 and not any(path_to_check.colliderect(piece.collision_rect) 
													 for piece in waiting_player.pieces 
													 if piece != janggi_piece)):
							# consider move limitations based on conditions
							if (new_rect.collidepoint(mouse_pos) and
		   						condition == "None" or
								condition == "Bikjang" and move_can_break_bikjang(active_player, waiting_player, janggi_piece, new_spot) or
								(condition == "Check" and (move_can_break_check(active_player, waiting_player, board, janggi_piece, new_spot))  or 
								find_piece_to_break_check(active_player, waiting_player, board) == janggi_piece)):
									# update piece location and collision for valid move
									temp = janggi_piece.location
									temp_rect = janggi_piece.collision_rect.topleft

									janggi_piece.location = new_spot
									janggi_piece.collision_rect.topleft = new_spot

									# make sure move does not leave own king vulnerable, cancel move if it does
									if (detect_check(active_player, waiting_player, board) and 
										find_piece_causing_check(active_player, waiting_player, board).location != janggi_piece.location):
										janggi_piece.location = temp
										janggi_piece.collision_rect.topleft = temp_rect
										
									# valid move was made
									else:
										# now check if the valid move resulted in a capture
										if detect_capture(waiting_player, janggi_piece):
											capture_piece(waiting_player, janggi_piece)

										# valid move was made
										return True
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked cannon piece to a valid location
# INPUT: piece, board, mouse position on window, player, waiting player, game cond
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_cannon(janggi_piece, board, mouse_pos, active_player, waiting_player, condition="None"):
	# implement logic here
	possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Get a list of all the pieces on the board
	all_pieces = active_player.pieces + waiting_player.pieces

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
									if not any(new_rect.colliderect(piece.collision_rect) 
																for piece in active_player.pieces 
																if piece != janggi_piece):
										
										# Check if this is the destination (the spot clicked by the mouse)
										# consider move limitations based on conditions
										if (new_rect.collidepoint(mouse_pos) and
											condition == "None" or
											condition == "Bikjang" and move_can_break_bikjang(active_player, waiting_player, janggi_piece, new_spot) or
											condition == "Check" and move_can_break_check(active_player, waiting_player, board, janggi_piece, new_spot)):
												# update piece location and collision for valid move
												temp = janggi_piece.location
												temp_rect = janggi_piece.collision_rect.topleft

												janggi_piece.location = new_spot
												janggi_piece.collision_rect.topleft = new_spot

												# make sure move does not leave own king vulnerable, cancel move if it does
												if (detect_check(active_player, waiting_player, board) and 
													find_piece_causing_check(active_player, waiting_player, board).location != janggi_piece.location):
													janggi_piece.location = temp
													janggi_piece.collision_rect.topleft = temp_rect
													
												# valid move was made
												else:
													# now check if the valid move resulted in a capture
													if detect_capture(waiting_player, janggi_piece):
														capture_piece(waiting_player, janggi_piece)

													# valid move was made
													return True

									# Keep moving
									new_rank += move[0]
									new_file += move[1]

								# There was a piece there, so try to capture it.	
								else:
									new_spot = board.coordinates[new_rank][new_file]
									new_rect = board.collisions[new_rank][new_file]
									for check_piece in all_pieces:
										if ((not any(new_rect.colliderect(piece.collision_rect) for piece in active_player.pieces if piece != janggi_piece)) 
																				and (check_piece.piece_type.value != "Cannon")
																				and (board.coordinates[new_rank][new_file] == check_piece.location)):
											# Check if this is the destination (the spot clicked by the mouse)
											# consider move limitations based on conditions
											if (new_rect.collidepoint(mouse_pos) and
												condition == "None" or
												condition == "Bikjang" and move_can_break_bikjang(active_player, waiting_player, janggi_piece, new_spot) or
												condition == "Check" and move_can_break_check(active_player, waiting_player, board, janggi_piece, new_spot)):
													# update piece location and collision for valid move
													temp = janggi_piece.location
													temp_rect = janggi_piece.collision_rect.topleft

													janggi_piece.location = new_spot
													janggi_piece.collision_rect.topleft = new_spot

													# make sure move does not leave own king vulnerable, cancel move if it does
													if (detect_check(active_player, waiting_player, board) and 
														find_piece_causing_check(active_player, waiting_player, board).location != janggi_piece.location):
														janggi_piece.location = temp
														janggi_piece.collision_rect.topleft = temp_rect
														
													# valid move was made
													else:
														# now check if the valid move resulted in a capture
														if detect_capture(waiting_player, janggi_piece):
															capture_piece(waiting_player, janggi_piece)

														# valid move was made
														return True
									break		

							# Return back to move-in-possible-moves loop so it cant skip pieces
							break
						else:
							# Continue moving in the current direction if no piece is found
							new_rank += move[0]
							new_file += move[1]
							
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked chariot piece to a valid location
# INPUT: piece, board, mouse position on window, player, waiting player, game cond
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_chariot(janggi_piece, board, mouse_pos, active_player, waiting_player, condition="None"):
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
								   for piece in active_player.pieces if piece != janggi_piece):
								break  # Stop if there's a piece possible the way
							
							# Check if this is the destination (the spot clicked by the mouse)
							# consider move limitations based on conditions
							if (new_rect.collidepoint(mouse_pos) and
		   						condition == "None" or
								condition == "Bikjang" and move_can_break_bikjang(active_player, waiting_player, janggi_piece, new_spot) or
								condition == "Check" and move_can_break_check(active_player, waiting_player, board, janggi_piece, new_spot)):
									# update piece location and collision for valid move
									temp = janggi_piece.location
									temp_rect = janggi_piece.collision_rect.topleft

									janggi_piece.location = new_spot
									janggi_piece.collision_rect.topleft = new_spot

									# make sure move does not leave own king vulnerable, cancel move if it does
									if (detect_check(active_player, waiting_player, board) and 
										find_piece_causing_check(active_player, waiting_player, board).location != janggi_piece.location):
										janggi_piece.location = temp
										janggi_piece.collision_rect.topleft = temp_rect
										
									# valid move was made
									else:
										# now check if the valid move resulted in a capture
										if detect_capture(waiting_player, janggi_piece):
											capture_piece(waiting_player, janggi_piece)

										# valid move was made
										return True

							# Stop if there's an opponent's piece (can move here but not beyond)
							if any(new_rect.colliderect(piece.collision_rect) 
								   for piece in waiting_player.pieces):
								break
						else:
							break  # Out of board bounds, stop in this direction
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked pawn piece to a valid location
# INPUT: piece, board, mouse position on window, player, waiting player, game cond
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_pawn(janggi_piece, board, mouse_pos, active_player, waiting_player, condition="None"):
	# Possible moves for the piece based on current possition (L/R/U)
	# view board as vertical (standard) where top of board is beginning of
	# the 2D list
	# (-x, y) --> left x spots
	# (+x, y) --> right x spots
	# (x, -y) --> up y spots
	# (x, +y) --> down y spots
	if active_player.board_perspective == "Bottom":
		palace = board.top_palace
		#				 ((Left),   (Up),  (Right))
		possible_moves = ((-1, 0), (0, -1), (1, 0))
	else:
		palace = board.bottom_palace
		
		#				 ((Left),   (Down),  (Right))
		possible_moves = ((-1, 0), (0, 1), (1, 0))


	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(board.coordinates):
		for file, spot in enumerate(row):
			# find where piece is relative to board
			if spot == janggi_piece.location:
				
				# if the pawn is in a palace, it can take palace moves
				if can_use_palace_diagonals(janggi_piece, palace):
					if move_pawn_palace(active_player, waiting_player, janggi_piece, board, mouse_pos, condition):
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
														for piece in active_player.pieces 
														if piece != janggi_piece)):
								# consider move limitations based on conditions
								if (condition == "None" or
									condition == "Bikjang" and move_can_break_bikjang(active_player, waiting_player, janggi_piece, new_spot) or
									condition == "Check" and move_can_break_check(active_player, waiting_player, board, janggi_piece, new_spot)):
										# update piece location and collision for valid move
										temp = janggi_piece.location
										temp_rect = janggi_piece.collision_rect.topleft

										janggi_piece.location = new_spot
										janggi_piece.collision_rect.topleft = new_spot

										# make sure move does not leave own king vulnerable, cancel move if it does
										if (detect_check(active_player, waiting_player, board) and 
											find_piece_causing_check(active_player, waiting_player, board).location != janggi_piece.location):
											janggi_piece.location = temp
											janggi_piece.collision_rect.topleft = temp_rect
											
										# valid move was made
										else:
											# now check if the valid move resulted in a capture
											if detect_capture(waiting_player, janggi_piece):
												capture_piece(waiting_player, janggi_piece)

											# valid move was made
											return True
							
	# no valid move made
	return False

#-----------------------------------------------------------------------------------
# Function that will move a clicked pawn piece to a valid location given it can make
# a move diagonally within palace
# INPUT: piece, board, mouse position on window, player, waiting player, game cond
# OUTPUT: Piece is remapped to valid spot
#-----------------------------------------------------------------------------------
def move_pawn_palace(active_player, waiting_player, janggi_piece, board, mouse_pos, condition="None"):
	# define which palace to use based on active player's perspective
	# pawn will never be in own palace
	if active_player.board_perspective == "Top":
		palace = board.bottom_palace
		palace_collisions = board.bottom_palace_collisions

		#			   ((UpLeft),       (UpRight))
		palace_moves = ((-1, 1),		(1, 1))
	else:
		palace = board.top_palace
		palace_collisions = board.top_palace_collisions

		#			   ((DownLeft),     (DownRight))
		palace_moves = ((-1, -1),		(1, -1))

	# find piece location relative to palace
	for rank, row in enumerate(palace):
		for file, spot in enumerate(row):
			if spot == janggi_piece.location:
				# verify the palace diagonal piece can make
				for move in palace_moves:
					new_rank = rank + move[0]
					new_file = file + move[1]
					# check that move location is in board
					if ((0 <= new_rank < len(palace))
						and (0 <= new_file < len(row))
						and (is_inside_palace(palace, new_rank, new_file))):
						# spot in palace
						new_spot = palace[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = palace_collisions[new_rank][new_file]
									
						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if (new_rect.collidepoint(mouse_pos)
							and not any(new_rect.colliderect(piece.collision_rect) 
										for piece in active_player.pieces 
										if piece != janggi_piece)):
							
							# consider move limitations based on conditions
							if (condition == "None" or
								condition == "Bikjang" and move_can_break_bikjang(active_player, waiting_player, janggi_piece, new_spot) or
								condition == "Check" and move_can_break_check(active_player, waiting_player, board, janggi_piece, new_spot)):
									# update piece location and collision for valid move
									temp = janggi_piece.location
									temp_rect = janggi_piece.collision_rect.topleft

									janggi_piece.location = new_spot
									janggi_piece.collision_rect.topleft = new_spot

									# make sure move does not leave own king vulnerable, cancel move if it does
									if (detect_check(active_player, waiting_player, board) and 
										find_piece_causing_check(active_player, waiting_player, board).location != janggi_piece.location):
										janggi_piece.location = temp
										janggi_piece.collision_rect.topleft = temp_rect
										
									# valid move was made
									else:
										# now check if the valid move resulted in a capture
										if detect_capture(waiting_player, janggi_piece):
											capture_piece(waiting_player, janggi_piece)

										# valid move was made
										return True
						
	# no valid move was made
	return False

#-----------------------------------------------------------------------------------
# Function that will determine if a move resides within the palace boundaries
# INPUT: board object, x coord of move, y coord of move
# OUTPUT: Boolean returned of whther move resides in a palace
#-----------------------------------------------------------------------------------
def is_inside_palace(palace, new_rank, new_file):
	# check if piece resides in palace
	for rank, row in enumerate(palace):
		for file, spot in enumerate(row):
			if (new_rank, new_file) == (rank, file):
				return True
			
	# outside of palace	
	return False

#-----------------------------------------------------------------------------------
# Function that will determine if the piece is in the diagonal spots of the palace,
# meaning that the piece can now move diagonally along the palace in given spots 
# INPUT: Piece object being moved, the palace
# OUTPUT: Boolean representing spot check result for that piece
#-----------------------------------------------------------------------------------		
def can_use_palace_diagonals(piece, palace):
	# palace diagonal spots
	diagonal_move_spots = (
								palace[0][0],			palace[0][2],

												palace[1][1],

								palace[2][0], 			palace[2][2]
							  )

	# determine if piece is in a diagonal spot in either palace
	for spot in diagonal_move_spots:
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
# INPUT: waiting player, piece that was moved
# OUTPUT: Boolean value returned, True if collides, False if not
#-----------------------------------------------------------------------------------
def detect_capture(waiting_player, piece):
	# detect if player captured a piece if they moved piece
	for janggi_piece in waiting_player.pieces:
		if piece.collision_rect.colliderect(janggi_piece.collision_rect):
			return True
	return False

#-----------------------------------------------------------------------------------
# Function that will perform the capturing of a piece
# INPUT: player whose turn it is, waiting player, piece that was moved
# OUTPUT: Piece is removed from waiting player's field of play
#-----------------------------------------------------------------------------------
def capture_piece(waiting_player, piece):
	# detect if player captured a piece if they moved piece
	for janggi_piece in waiting_player.pieces:
		if piece.collision_rect.colliderect(janggi_piece.collision_rect):
			waiting_player.pieces.remove(janggi_piece)
	
	return

#-----------------------------------------------------------------------------------
# Function that will check if Bikjang occurs. This occurs when the two King pieces
# are facing each other in the same column of the board with no pieces in the way
# INPUT: player whose turn it is, waiting player
# OUTPUT: Boolean value returned, True if Bikjang, False if not
#-----------------------------------------------------------------------------------
def detect_bikjang(active_player, waiting_player):
	player_king_location = None
	opponent_king_location = None

	# find player's king location
	for janggi_piece in active_player.pieces:
		if janggi_piece.piece_type.value == "King":
			player_king_location = janggi_piece.location
			break

	# find opponent's king location
	for janggi_piece in waiting_player.pieces:
		if janggi_piece.piece_type.value == "King":
			opponent_king_location = janggi_piece.location
			break

	if player_king_location and opponent_king_location:
		# check if both kings are in the same column
		if player_king_location[0] == opponent_king_location[0]:
			# get the range between the kings' row positions
			min_row = min(player_king_location[1], opponent_king_location[1])
			max_row = max(player_king_location[1], opponent_king_location[1])

			# check for any possible pieces in the same column between the kings
			for janggi_piece in active_player.pieces + waiting_player.pieces:
				if janggi_piece.location[0] == player_king_location[0]:
					if min_row < janggi_piece.location[1] < max_row:
						return False
					
			# no possible pieces found, Bikjang occurs
			return True

	# default to Bikjang not occurring if conditions aren't met
	return False

#-----------------------------------------------------------------------------------
# Function that will check if a piece moved cause a check state
# INPUT: player, waiting player, board
# OUTPUT: Boolean returned for check state
#-----------------------------------------------------------------------------------
def detect_check(active_player, waiting_player, board):
	# get a list of all the possible move-to locations by the waiting player
	threatening_spaces = get_all_possible_moves(waiting_player, active_player, board)

	# find the active player's king
	player_king_location = None

	# find player's king location
	for janggi_piece in active_player.pieces:
		if janggi_piece.piece_type.value == "King":
			player_king_location = janggi_piece.location
			break

	# check if the active player's king is in any of the threatening spaces
	if any(space == player_king_location for space in threatening_spaces):
		return True # in check
	
	# default to not in check
	return False # not in check

#-----------------------------------------------------------------------------------
# Function that will handle any urgent game conditions (Bikjang, Check, etc...)
# INPUT: player, waiting player, board
# OUTPUT: return a flag on whether the condition was resolved
#-----------------------------------------------------------------------------------
def resolve_condition(active_player, waiting_player, board, condition = "None"):
	# check and handle Bikjang
	if condition == "Bikjang":
		possible_moves = get_all_possible_moves(active_player, waiting_player, board)
		if not breakable_bikjang(active_player, waiting_player, possible_moves):
			return False # bikjang cannot be broken, game over as draw
	
	# check and handle Check
	elif condition == "Check":
		possible_moves = get_all_possible_moves(active_player, waiting_player, board)
		if not breakable_check(active_player, waiting_player, board):
			return False # check cannot be broken, game over as checkmate

	return True

#-----------------------------------------------------------------------------------
# Function that will get all move locations for every piece on the board of one color
# INPUT: player, waiting player, board
# OUTPUT: all possible moves for the player as a list of tuples
#-----------------------------------------------------------------------------------
def get_all_possible_moves(active_player, waiting_player, board):
	possible_moves = list()
	# get every possible move for each of the player's pieces
	for janggi_piece in active_player.pieces:
		if janggi_piece.piece_type.value == "King":
			possible_moves += (king_possible_moves(janggi_piece, board, active_player))
		elif janggi_piece.piece_type.value == "Advisor":
			possible_moves += (advisor_possible_moves(janggi_piece, board, active_player))
		elif janggi_piece.piece_type.value == "Elephant":
			possible_moves += (elephant_possible_moves(janggi_piece, board, active_player, waiting_player))
		elif janggi_piece.piece_type.value == "Horse":
			possible_moves += (horse_possible_moves(janggi_piece, board, active_player, waiting_player))
		elif janggi_piece.piece_type.value == "Cannon":
			possible_moves += (cannon_possible_moves(janggi_piece, board, active_player, waiting_player))
		elif janggi_piece.piece_type.value == "Chariot":
			possible_moves += (chariot_possible_moves(janggi_piece, board, active_player, waiting_player))
		elif janggi_piece.piece_type.value == "Pawn":
			possible_moves += (pawn_possible_moves(janggi_piece, board, active_player))
			
	# return all possible moves for the player as a list of tuples
	return list(possible_moves)

#-----------------------------------------------------------------------------------
# Function that will get the theoretical moves for the king piece
# INPUT: king piece, board, player
# OUTPUT: all possible moves for the king piece as a list of tuples
#-----------------------------------------------------------------------------------
def king_possible_moves(janggi_piece, board, player):
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
	
	# set that will hold all possible moves for ending the condition
	moves = set()

	# define which palace to use based on active player's perspective
	if player.board_perspective == "Bottom":
		palace = board.bottom_palace
		palace_collisions = board.bottom_palace_collisions
	else:
		palace = board.top_palace
		palace_collisions = board.top_palace_collisions

	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(palace):
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
					if ((0 <= new_rank < len(palace))
							and (0 <= new_file < len(row))):
						# spot in board
						new_spot = palace[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = palace_collisions[new_rank][new_file]

						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if (not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)):
							
							# place coordinates into the set to avoid duplicates
							moves.add(new_spot)
						
	# no valid move was made
	#print(f"KING MOVES: {moves}")
	return list(moves)

#-----------------------------------------------------------------------------------
# Function that will get the theoretical moves for the advisor piece
# INPUT: advisor piece, board, player
# OUTPUT: all possible moves for the advisor piece as a list of tuples
#-----------------------------------------------------------------------------------
def	advisor_possible_moves(janggi_piece, board, player):
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
	
	# set that will hold all possible moves for ending the condition
	moves = set()

	# define which palace to use based on active player's perspective
	if player.board_perspective == "Bottom":
		palace = board.bottom_palace
		palace_collisions = board.bottom_palace_collisions
	else:
		palace = board.top_palace
		palace_collisions = board.top_palace_collisions

	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(palace):
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
					if ((0 <= new_rank < len(palace))
							and (0 <= new_file < len(row))):
						# spot in board
						new_spot = palace[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = palace_collisions[new_rank][new_file]

						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if (not any(new_rect.colliderect(piece.collision_rect) 
													 for piece in player.pieces 
													 if piece != janggi_piece)):
							# place coordinates into the list
							moves.add(new_spot)
						
	# no valid move was made
	return list(moves)

#-----------------------------------------------------------------------------------
# Function that will get the theoretical moves for the elephant piece
# INPUT: elephant piece, board, player, opponent
# OUTPUT: all possible moves for the elephant piece as a list of tuples
#-----------------------------------------------------------------------------------
def elephant_possible_moves(janggi_piece, board, player, opponent):
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

	# set that will hold all possible moves for ending the condition
	moves = set()

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
							# add moves for condition to set
							moves.add(new_spot)
						
	# no valid move was made
	return list(moves)

#-----------------------------------------------------------------------------------
# Function that will get the theoretical moves for the horse piece
# INPUT: horse piece, board, player, opponent
# OUTPUT: all possible moves for the horse piece as a list of tuples
#-----------------------------------------------------------------------------------
def horse_possible_moves(janggi_piece, board, player, opponent):
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

	# set that will hold all possible moves for ending the condition
	moves = set()

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
			
							# add moves for condition to set
							moves.add(new_spot)
						
	# no valid move was made
	return list(moves)

#-----------------------------------------------------------------------------------
# Function that will get the theoretical moves for the cannon piece
# INPUT: cannon piece, board, player, opponent
# OUTPUT: all possible moves for the cannon piece as a list of tuples
#-----------------------------------------------------------------------------------
def cannon_possible_moves(janggi_piece, board, player, opponent):
	# implement logic here
	possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

	# set that will hold all possible moves for ending the condition
	moves = set()

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
									if not any(new_rect.colliderect(piece.collision_rect) 
																for piece in player.pieces 
																if piece != janggi_piece):
										# place coordinates into the list
										moves.add(new_spot)
									

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
												
											# place coordinates into the list
											moves.add(new_spot)
									break		

							# Return back to move-in-possible-moves loop so it cant skip pieces
							break
						else:
							# Continue moving in the current direction if no piece is found
							new_rank += move[0]
							new_file += move[1]
							
	return list(moves)
	
#-----------------------------------------------------------------------------------
# Function that will get the theoretical moves for the chariot piece
# INPUT: chariot piece, board, player, opponent
# OUTPUT: all possible moves for the chariot piece as a list of tuples
#-----------------------------------------------------------------------------------
def chariot_possible_moves(janggi_piece, board, player, opponent):
	# Define rook-like moves for chariot (up, down, left, right)
	rook_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
	diagonal_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

	# set that will hold all possible moves for ending the condition
	moves = set()

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
								break  # Stop if there's a piece possible the way
							
							moves.add(new_spot)

							# Stop if there's an opponent's piece (can move here but not beyond)
							if any(new_rect.colliderect(piece.collision_rect) 
								   for piece in opponent.pieces):
								break
						else:
							break  # Out of board bounds, stop in this direction
	return list(moves)

#-----------------------------------------------------------------------------------
# Function that will get the theoretical moves for the pawn piece
# INPUT: pawn piece, board, player
# OUTPUT: all possible moves for the pawn piece as a list of tuples
#-----------------------------------------------------------------------------------
def pawn_possible_moves(janggi_piece, board, player):
	# Possible moves for the piece based on current possition (L/R/U)
	# view board as vertical (standard) where top of board is beginning of
	# the 2D list
	# (-x, y) --> left x spots
	# (+x, y) --> right x spots
	# (x, -y) --> up y spots
	# (x, +y) --> down y spots
	if player.board_perspective == "Bottom":
		palace = board.top_palace
		#				 ((Left),   (Up),  (Right))
		possible_moves = ((-1, 0), (0, -1), (1, 0))
	else:
		palace = board.bottom_palace
		
		#				 ((Left),   (Down),  (Right))
		possible_moves = ((-1, 0), (0, 1), (1, 0))

	# set that will hold all possible moves for ending the condition
	moves = set()

	# Check each spot in the board for valid locations where
	# rank is the row, and file is the spot in that row
	# i.e Cho King starts at Rank 9/File 5
	for rank, row in enumerate(board.coordinates):
		for file, spot in enumerate(row):
			# find where piece is relative to board
			if spot == janggi_piece.location:
				
				# if the pawn is in a palace, it can take palace moves
				if can_use_palace_diagonals(janggi_piece, palace):
					 # place coordinates into the list
					moves.update(pawn_palace_possible_moves(player, janggi_piece, board))
					
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
							if (not any(new_rect.colliderect(piece.collision_rect) 
														for piece in player.pieces 
														if piece != janggi_piece)):
								# place coordinates into the list
								moves.add(new_spot)
							
	# no valid move made
	return list(moves)

#-----------------------------------------------------------------------------------
# Function that will get the theoretical moves for the pawn piece given in a palace
# INPUT: player, pawn piece, board
# OUTPUT: all possible moves for the pawn piece as a list of tuples
#-----------------------------------------------------------------------------------
def pawn_palace_possible_moves(player, janggi_piece, board):
	# define which palace to use based on active player's perspective
	# pawn will never be in own palace
	if player.board_perspective == "Top":
		palace = board.bottom_palace
		palace_collisions = board.bottom_palace_collisions

		#			   ((UpLeft),       (UpRight))
		palace_moves = ((-1, 1),		(1, 1))
	else:
		palace = board.top_palace
		palace_collisions = board.top_palace_collisions

		#			   ((DownLeft),     (DownRight))
		palace_moves = ((-1, -1),		(1, -1))

	# set that will hold all possible moves for ending the condition
	moves = set()

	# find piece location relative to palace
	for rank, row in enumerate(palace):
		for file, spot in enumerate(row):
			if spot == janggi_piece.location:
				# verify the palace diagonal piece can make
				for move in palace_moves:
					new_rank = rank + move[0]
					new_file = file + move[1]
					# check that move location is in board
					if ((0 <= new_rank < len(palace))
						and (0 <= new_file < len(row))
						and (is_inside_palace(palace, new_rank, new_file))):
						# spot in palace
						new_spot = palace[new_rank][new_file]
						# collision rectangle for the spot
						new_rect = palace_collisions[new_rank][new_file]
									
						# Make sure spot is not occupied by another piece of the player
						# but exclude the piece being moved from being checked
						if (not any(new_rect.colliderect(piece.collision_rect) 
										for piece in player.pieces 
										if piece != janggi_piece)):
							
							# add moves for condition to set
							moves.add(new_spot)
						
	# no valid move was made
	return list(moves)

#-----------------------------------------------------------------------------------
# Function that will get the theoretical moves to break a Bikjang condition
# INPUT: player under bikjang, waiting player, player's possible moves, condition
# OUTPUT: list of tuples of the possible moves that will break the Bikjang
#-----------------------------------------------------------------------------------
def bikjang_moves(active_player, waiting_player, possible_moves, condition):
	if condition == "None":
		return possible_moves
	else:
		for move in possible_moves:
			# check if the player can break the Bikjang
			if not move_can_break_bikjang(active_player, waiting_player, move):
				possible_moves.remove(move)
			else:
				# player cannot break the Bikjang, remove all moves
				return []

#-----------------------------------------------------------------------------------
# Function that will test a given move to break a Bikjang condition
# INPUT: player under bikjang, waiting player, piece moving, move by piece
# OUTPUT: Boolean on whether the move can break the Bikjang
#-----------------------------------------------------------------------------------
def move_can_break_bikjang(active_player, waiting_player, janggi_piece, move):
	player_king_location = None
	opponent_king_location = None

	# Find player's king location
	for piece in active_player.pieces:
		if piece.piece_type.value == "King":
			player_king_location = piece.location
			break

	# Find opponent's king location
	for piece in waiting_player.pieces:
		if piece.piece_type.value == "King":
			opponent_king_location = piece.location
			break

	# get the space between the kings
	min_row = min(player_king_location[1], opponent_king_location[1])
	max_row = max(player_king_location[1], opponent_king_location[1])

	# check if a possible move can be made to break the Bikjang
	if move[0] == player_king_location[0]:
		if min_row < move[1] < max_row:
			# Bikjang can be broken
			return True 
		
	# handle case where player moves king L/R to break Bikjang
	if janggi_piece.piece_type.value == "King" and move[0] != player_king_location[0]:
		return True
	
	# default to move cannot break Bikjang if conditions aren't met
	return False

#-----------------------------------------------------------------------------------
# Function that will test a given move to break a Check condition
# INPUT: player under check, waiting player,board, piece moving, move by piece
# OUTPUT: Boolean on whether the move can break the Check condition
#-----------------------------------------------------------------------------------
def move_can_break_check(active_player, waiting_player, board, janggi_piece, new_spot):
	# check if a possible move can be made to break the check PAWN
	possible_moves = []
	match janggi_piece.piece_type.value:
		case "King":
			possible_moves = king_possible_moves(janggi_piece, board, active_player)
		case "Advisor":
			possible_moves = advisor_possible_moves(janggi_piece, board, active_player)
		case "Elephant":
			possible_moves = elephant_possible_moves(janggi_piece, board, active_player, waiting_player)
		case "Horse":
			possible_moves = horse_possible_moves(janggi_piece, board, active_player, waiting_player)
		case "Cannon":
			possible_moves = cannon_possible_moves(janggi_piece, board, active_player, waiting_player)
		case "Chariot":
			possible_moves = chariot_possible_moves(janggi_piece, board, active_player, waiting_player)
		case "Pawn":
			possible_moves = pawn_possible_moves(janggi_piece, board, active_player)

	# get all the moves that can be made from waiting player
	threatening_spaces = get_all_possible_moves(waiting_player, active_player, board)

	# find spot piece can move to that will end the check
	possible_moves = [spot for spot in possible_moves if spot not in threatening_spaces]

	# get piece threathening king
	threatening_piece = find_piece_causing_check(active_player, waiting_player, board)

	# king will have special functionality when atempting to move on a check
	if janggi_piece.piece_type.value == "King":

		# cover edge case special conditions for cannon
		# a cannon needs a piece in order to jump over and capture the king
			# The king may be considered a screen in this scenario and therefore any spot behind
			# the king would be detected as invalid, so we should exclude that case
			# this will be anytime the king and an enemy cannon face each other
		screened_cannons = get_screened_cannon(waiting_player)
		if len(screened_cannons) > 0:
			for cannon in screened_cannons:
				facing_cannon_spots = cannon_possible_moves(cannon, board, waiting_player, active_player)
				threatening_spaces = [spot for spot in threatening_spaces if spot not in facing_cannon_spots]


		# cover edge case special conditions for chariot threatening the king
		if threatening_piece.piece_type.value == "Chariot":
			# if king can capture piece
			if new_spot == threatening_piece.location and new_spot in possible_moves:
				return True
			# king cannot move along the same column/row as the threatening chariot, but can capture it
			elif (new_spot[0] == threatening_piece.location[0] or new_spot[1] == threatening_piece.location[1]):
				return False
			
		# search for an open space to move the king to
		if new_spot in possible_moves:
			return True
		
	# non-king piece is clicked
	else:
		# cover edge case special conditions for cannon
		if threatening_piece.piece_type.value == "Cannon":
			# a cannon needs a piece in order to jump over and capture the king, we should
			# check if the current janggi_piece is that screen, where the player can simply move it out to remove the check
			# we should check if the piece can move outside the same row/column that the cannon is in
			if new_spot[0] != threatening_piece.location[0] and new_spot[1] != threatening_piece.location[1]:
				# proceed with normal check
				if new_spot in possible_moves:
					return True
				else:
					return False
				
		# is the space available
		if new_spot not in possible_moves:
			return True
		
	# default to move cannot break check if conditions aren't met
	return False

#-----------------------------------------------------------------------------------
# Function that will test whether a Bikjang condition can be broken
# INPUT: player under Bikjang, waiting player, list of tuples player's possible moves
# OUTPUT: Boolean on whether the Bikjang condition can be broken
#-----------------------------------------------------------------------------------
def breakable_bikjang(active_player, waiting_player, possible_moves):
	player_king_location = None
	opponent_king_location = None

	# find player's king location
	for janggi_piece in active_player.pieces:
		if janggi_piece.piece_type.value == "King":
			player_king_location = janggi_piece.location
			break

	# find opponent's king location
	for janggi_piece in waiting_player.pieces:
		if janggi_piece.piece_type.value == "King":
			opponent_king_location = janggi_piece.location
			break

	if player_king_location and opponent_king_location:
		# check if both kings are in the same column
		if player_king_location[0] == opponent_king_location[0]:
			# get the range between the kings' row positions
			min_row = min(player_king_location[1], opponent_king_location[1])
			max_row = max(player_king_location[1], opponent_king_location[1])

			# cover edge case where a single coordinate is passed
			if len(possible_moves) == 2:
				if possible_moves[0] == player_king_location[0]:
					if min_row < possible_moves[1] < max_row:
						# Bikjang can be broken
						return True 

			else:
				# Check for any possible pieces in the same column between the kings
				for location in possible_moves:
					if location[0] == player_king_location[0]:
						if min_row < location[1] < max_row:
							# Bikjang can be broken
							return True 
			
			# Bikjang cannot be broken, results in tie
			return False

	# default to Bikjang not breakable if conditions aren't met
	return False

#-----------------------------------------------------------------------------------
# Function that will find the piece causing the Check condition
# INPUT: player under check, waiting player, board
# OUTPUT: piece object that is causing the Check condition
#-----------------------------------------------------------------------------------
def find_piece_causing_check(active_player, waiting_player, board):
	# king in check
	checked_king = None

	# find the king that is in check
	for janggi_piece in active_player.pieces:
		if janggi_piece.piece_type.value == "King":
			checked_king = janggi_piece

	if checked_king is not None:
		# check each of checked player's pieces
		for janggi_piece in waiting_player.pieces:
			# check each move for the piece to see if it can break the check
			match janggi_piece.piece_type.value:
				case "Elephant":
					possible_moves = elephant_possible_moves(janggi_piece, board, waiting_player, active_player)
					for spot in possible_moves:
						if spot == checked_king.location:
							return janggi_piece
				case "Horse":
					possible_moves = horse_possible_moves(janggi_piece, board, waiting_player, active_player)
					for spot in possible_moves:
						if spot == checked_king.location:
							return janggi_piece
				case "Cannon":
					possible_moves = cannon_possible_moves(janggi_piece, board, waiting_player, active_player)
					for spot in possible_moves:
						if spot == checked_king.location:
							return janggi_piece
				case "Chariot":
					possible_moves = chariot_possible_moves(janggi_piece, board, waiting_player, active_player)
					for spot in possible_moves:
						if spot == checked_king.location:
							return janggi_piece
				case "Pawn":
					possible_moves = pawn_possible_moves(janggi_piece, board, waiting_player)
					for spot in possible_moves:
						if spot == checked_king.location:
							return janggi_piece
				case _:
					pass

	# no piece can break the check, try moving the king next
	return checked_king
	
#-----------------------------------------------------------------------------------
# Function that will find a piece that can break the Check condition by capture
# INPUT: player under check, waiting player, board
# OUTPUT: piece object that can capture the threatening piece
#-----------------------------------------------------------------------------------
def find_piece_to_break_check(active_player, waiting_player, board):
	# piece threatening king
	threatening_piece = find_piece_causing_check(active_player, waiting_player, board)
	# check each of checked player's pieces
	for janggi_piece in active_player.pieces:
		# check each move for the piece to see if it can break the check
		match janggi_piece.piece_type.value:
			case "Elephant":
				possible_moves = elephant_possible_moves(janggi_piece, board, active_player, waiting_player)
				for spot in possible_moves:
					if spot == threatening_piece.location:
						return janggi_piece
			case "Horse":
				possible_moves = horse_possible_moves(janggi_piece, board, active_player, waiting_player)
				for spot in possible_moves:
					if spot == threatening_piece.location:
						return janggi_piece
			case "Cannon":
				possible_moves = cannon_possible_moves(janggi_piece, board, active_player, waiting_player)
				for spot in possible_moves:
					if spot == threatening_piece.location:
						return janggi_piece
			case "Chariot":
				possible_moves = chariot_possible_moves(janggi_piece, board, active_player, waiting_player)
				for spot in possible_moves:
					if spot == threatening_piece.location:
						return janggi_piece
			case "Pawn":
				possible_moves = pawn_possible_moves(janggi_piece, board, active_player)
				for spot in possible_moves:
					if spot == threatening_piece.location:
						return janggi_piece

	# no piece can capture the check
	return threatening_piece
	
#-----------------------------------------------------------------------------------
# Function that determine if a Check state can be broken
# INPUT: player under check, waiting player, board
# OUTPUT: Boolean on whether the Check state can be broken
#-----------------------------------------------------------------------------------
def breakable_check(active_player, waiting_player, board):
	# king in check
	checked_king = None

	# find the player's king that is in check
	for janggi_piece in active_player.pieces:
		if janggi_piece.piece_type.value == "King":
			checked_king = janggi_piece

	# an unbreakable check occurs when there are no possible moves that can be made to break check
	possible_moves = get_all_possible_moves(active_player, waiting_player, board)
	for move in possible_moves:
		if move_can_break_check(active_player, waiting_player, board, checked_king, move):
			return True

	return False
	
#-----------------------------------------------------------------------------------
# Function that will find the cannons of one side that have "screens"
# INPUT: player to check the cannons of
# OUTPUT: list of the cannon objects that have screens
#-----------------------------------------------------------------------------------
def get_screened_cannon(player):

	cannons = list()
	# find opposing cannon locations
	for piece in player.pieces:
		if piece.piece_type.value == "Cannon":
			cannons.append(piece)

	# check if the piece is facing a cannon (screen for a cannon)
	for cannon in cannons:
		if(piece.location[0] != cannon.location[0] or
	 		piece.location[1] != cannon.location[1]):
			cannons.remove(cannon)

	return list(cannons)

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

#-----------------------------------------------------------------------------------
# Function that will get the center location of the display window for mapping UI
# INPUT: None
# OUTPUT: center location of window surface as tuple
#-----------------------------------------------------------------------------------
def get_window_center_location():
	# return a reference to the center of the screen
	window = pygame.display.set_mode((constants.screen_width, constants.screen_height))
	center_loc = window.get_rect().center
	pygame.display.quit()
	return center_loc

#-----------------------------------------------------------------------------------
# Function that will get the center location of a loaded image for mapping UI
# INPUT: image surface object
# OUTPUT: center location of image surface as tuple
#-----------------------------------------------------------------------------------
def get_image_center_location(image):
	# return a reference to the center of the image
	center_loc = image.get_rect().center
	return center_loc