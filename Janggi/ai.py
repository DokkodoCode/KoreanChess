import subprocess
import board
import pygame
import re
import numpy as np

from piece import Piece, PieceCollisionSize, PieceType, OpponentPiecePosition
from helper_funcs import reformat_piece_collision

#######		Please Read		########
# Update if changed

# Class functionality is used in the SinglePlayerGame class in state.py in an if-statement.
# To read the AI move, 'a-f' is read from right to left with 'a' being on the right. '1-9' is read 
# from bottom to top, with '1' being at the bottom and '9' at the top. 
# The AI currently gives moves for the player to do, which can be changed by changing colors.

class OpponentAI:
	def __init__(self, is_host=False, board_perspective="Top", difficulty="easy", color="Han"):
		self.difficulty = difficulty
		self.color = color
		self.color = color
		self.is_host = is_host
		self.board_perspective = board_perspective
		self.piece_convention = "International"
		self.ai_level = None
		self.is_ready = False
		self.is_clicked = False
		self.is_turn = False
		self.initiated_bikjang = False
		self.is_checked = False
		self.pieces = self.fill_pieces()
		# self.settings = self.initialize_settings()

		# Start the engine process
		# Formality stuff
		self.engine = subprocess.Popen(
			["./fairy-stockfish-largeboard_x86-64"],
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True
		)
		if color == "Han":
			self.fen_color = "w"
		else:
			self.fen_color = "b"
		self.is_turn = False
		self.pieces = self.fill_pieces()

		# Initialize UCI mode and set the variant to Janggi.
		# This is just formality stuff
		self.send_command("uci")
		self.send_command("setoption name UCI_Variant value janggi")
		self.send_command("position startpos")

	def restart_engine(self):
		self.engine.terminate()
		self.engine = subprocess.Popen(
			["./fairy-stockfish-largeboard_x86-64"],
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True
		)

		self.send_command("uci")
		self.send_command("setoption name UCI_Variant value janggi")
		self.send_command("position startpos")

	# Method to populate the player's pieces for Janggi
	# INPUT: None
	# OUTPUT: A list of the piece objects
	def fill_pieces(self):
		pieces = [] # store the piece objects
	
		# for each piece in PieceType(enum) list
		for piece_type in PieceType:
			# lookup the list of starting positions based on the enum PieceType
			positions = OpponentPiecePosition[piece_type.name].value
			# iterate through that list of starting positions
			for pos in positions:
				# assign point value to current piece based on PieceType(enum)
				point_value = PieceType[piece_type.name].value
				# assign the location that piece will be and where to display its image
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
	
	# Function to get the best move from the engine.
	# The engine will output several lines. This searches the lines
	# to find the one labeled "bestmove", which we will use to update the board.
	# Best move will come out in a coordinate format similar to chess. eg. i3h3. 
	# which means move the piece at coordinate i3 to h3.
	def get_engine_move(self):
		while True:
			output = self.engine.stdout.readline().strip()
			if "bestmove" in output:
				best_move = output.split()[1]
				return best_move
	
	# Function for sending commands to the engine.
	def send_command(self, command):
		self.engine.stdin.write(command + '\n')
		self.engine.stdin.flush()

	# Clears Stockfish's output buffer
	def flush_engine_output(self):
		import time
		buffer = []
		start_time = time.time()

		while True:
			# Read a line from Stockfish's stdout
			line = self.engine.stdout.readline().strip()
			if line:  # If there's output, store it in the buffer
				buffer.append(line)
				print(f"Flushed line: {line}")  # Debugging log (optional)
			else:
				# If no output and we have waited long enough, break
				if time.time() - start_time > 0.5:  # Avoid hanging indefinitely
					break

		return buffer

	# Converts the h1d1 type stockifsh output to coordinates on the board
	def notation_to_coordinates(self, location):
		# Define column mappings for Janggi notation
		columns = {'i': 0, 'h': 1, 'g': 2, 'f': 3, 'e': 4, 'd': 5, 'c': 6, 'b': 7, 'a': 8}

		# Get map index value
		column = columns[location[:1]]
		row = int(location[1:]) - 1  # Convert "1" to index 0, etc.
		
		return (column, row)

	# Function to find the piece at the position given by the Stockfish notation
	def find_piece_on_board(self, player,  board, location):
		# 'location' is a rank and file
		# Find the piece by checking every self(opponent) piece location
		# against the location of the stockfish move.

		##### 
		# The self pieces and player pieces are flipped and its a problem
		#####
		for rank, row in enumerate(board.coordinates):
			for file, spot in enumerate(row):
				if (rank, file) == location:
					for piece in self.pieces:
						if piece.location == spot:
							return piece
		return
		
	# Convert the board class board of coordinates and pieces
	# into string format
	def convert_board(self, board, player):
		# Create a template for the board
		new_board = np.array([
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
		
		
		# Add the player's pieces to the template
		new_board = self.add_player_pieces(new_board, player, board, piece_type_mapping)
		# Add the opponent's pieces to the template
		new_board = self.add_opponent_pieces(new_board, board, piece_type_mapping)
		#new_board = self.test(new_board, player, board)
	
		return np.flipud(new_board)
	
	# def test(self, new_board, player, board):
	# 	pieces = self.pieces + player.pieces
	# 	for row in range(len(board.coordinates)):
	# 		for column in range(len(board.coordinates[row])):
	# 			for piece in pieces:
	# 				if board.coordinates[row][column] == piece.location:
	# 					new_board[column][row] = "X"
	# 	return new_board
	
	# Return the board with the players pieces added to the string
	def add_player_pieces(self, new_board, player, board, piece_type_mapping):
		for row in range(len(board.coordinates)):
			for column in range(len(board.coordinates[row])):
				for piece in player.pieces:
					if board.coordinates[row][column] == piece.location:
						new_board[column][row] = piece_type_mapping.get(piece.piece_type.value).lower()
		print(new_board)
		return new_board

	# Opponent is self here, I know the name may be confusing.
	# Return the board with the opponent's (self) pieces added to the string
	def add_opponent_pieces(self, new_board, board, piece_type_mapping):
		for row in range(len(board.coordinates)):
			for column in range(len(board.coordinates[row])):
				for piece in self.pieces:
					if board.coordinates[row][column] == piece.location:
						new_board[column][row] = piece_type_mapping.get(piece.piece_type.value)
		print("AI")
		print(new_board)
		return new_board

	# Function to generate FEN string from the board state
	# The FEN string is a way of recording the current board state in string format.
	# This string format is what is passed to stockfish so that it can make a move.
	def generate_fen(self, board):
		fen_rows = []
		for row in board:
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
		
		fen_string = "/".join(fen_rows) + " " + self.fen_color
		return fen_string





# Example board state
# We need to import the current board state and convert it into this format.
# janggi_board = [
# 	["r", "n", "b", "a", ".", "a", "b", "n", "r"],
# 	[".", ".", ".", ".", "k", ".", ".", ".", "."],
# 	[".", "c", ".", ".", ".", ".", ".", "c", "."],
# 	["p", ".", "p", ".", "p", ".", "p", ".", "p"],
# 	[".", ".", ".", ".", ".", ".", ".", ".", "."],
# 	[".", ".", ".", ".", ".", ".", ".", ".", "."],
# 	["P", ".", "P", ".", "P", ".", "P", ".", "P"],
# 	[".", "C", ".", ".", ".", ".", ".", "C", "."],
# 	[".", ".", ".", ".", "k", ".", ".", ".", "."],
# 	["R", "R", "R", "R", ".", "R", "B", "N", "R"],
# ]

# w means white in chess terms, in this case w = red.
# b meand black in chess terms, in this case b = blue
# This should be set to the opposite of what was chosen in the start
# menu by the player.


