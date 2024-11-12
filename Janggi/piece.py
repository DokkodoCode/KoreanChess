"""
-----------------------piece.py-----------------------------------
o This file is to hold the data for each piece in Janggi
o Last Modified - October 31st 2024
------------------------------------------------------------------
"""

# libraries
from enum import Enum

# local file imports, see individ file for details
import constants

# Enumeration type for the PieceType
class PieceType(Enum):
	KING = "King"
	ADVISOR = "Advisor"
	ELEPHANT = "Elephant"
	HORSE = "Horse"
	CANNON = "Cannon"
	CHARIOT = "Chariot"
	PAWN = "Pawn"

# Enumeration type for each piece's point value
class PieceValue(Enum):
	KING = 0
	ADVISOR = 3
	ELEPHANT = 3
	HORSE = 5
	CANNON = 7
	CHARIOT = 13
	PAWN = 2

# Enumeration type for the amount of each piece the player starts w/
class PieceCount(Enum):
	KING = 1
	ADVISOR = 2
	ELEPHANT = 2
	HORSE = 2
	CANNON = 2
	CHARIOT = 2
	PAWN = 5

# Enumeration type for each piece's display size
class PieceSize(Enum):
	KING = constants.large_size
	ADVISOR = constants.small_size
	ELEPHANT = constants.med_size
	HORSE = constants.med_size
	CANNON = constants.med_size
	CHARIOT = constants.med_size
	PAWN = constants.small_size

# Enumeration type for each piece's collision rectangle size
class PieceCollisionSize(Enum):
	KING = constants.large_collision_size
	ADVISOR = constants.small_collision_size
	ELEPHANT = constants.med_collision_size
	HORSE = constants.med_collision_size
	CANNON = constants.med_collision_size
	CHARIOT = constants.med_collision_size
	PAWN = constants.small_collision_size

# Enumeration type for each player-side piece's starting position
class PlayerPiecePosition(Enum):
	KING = [(constants.x_coordinates[4],constants.y_coordinates[8])]
	ADVISOR = [(constants.x_coordinates[3],constants.y_coordinates[9]),
				(constants.x_coordinates[5],constants.y_coordinates[9])]
	ELEPHANT = [(constants.x_coordinates[2],constants.y_coordinates[9]),
			 	(constants.x_coordinates[7],constants.y_coordinates[9])]
	HORSE = [(constants.x_coordinates[1],constants.y_coordinates[9]),
		  	(constants.x_coordinates[6],constants.y_coordinates[9])]
	CANNON = [(constants.x_coordinates[1],constants.y_coordinates[7]),
		   	(constants.x_coordinates[7],constants.y_coordinates[7])]
	CHARIOT = [(constants.x_coordinates[0],constants.y_coordinates[9]),
				(constants.x_coordinates[8],constants.y_coordinates[9])]
	PAWN = [(constants.x_coordinates[0],constants.y_coordinates[6]),
		 	(constants.x_coordinates[2],constants.y_coordinates[6]),
			(constants.x_coordinates[4],constants.y_coordinates[6]),
			(constants.x_coordinates[6],constants.y_coordinates[6]),
			(constants.x_coordinates[8],constants.y_coordinates[6])]

# Enumeration type for each opponent's piece's starting position
class OpponentPiecePosition(Enum):
	KING = [(constants.x_coordinates[4],constants.y_coordinates[1])]
	ADVISOR = [(constants.x_coordinates[3],constants.y_coordinates[0]),
				(constants.x_coordinates[5],constants.y_coordinates[0])]
	ELEPHANT = [(constants.x_coordinates[2],constants.y_coordinates[0]),
			 	(constants.x_coordinates[7],constants.y_coordinates[0])]
	HORSE = [(constants.x_coordinates[1],constants.y_coordinates[0]),
		  	 (constants.x_coordinates[6],constants.y_coordinates[0])]
	CANNON = [(constants.x_coordinates[1],constants.y_coordinates[2]),
		   	  (constants.x_coordinates[7],constants.y_coordinates[2])]
	CHARIOT = [(constants.x_coordinates[0],constants.y_coordinates[0]),
				(constants.x_coordinates[8],constants.y_coordinates[0])]
	PAWN = [(constants.x_coordinates[0],constants.y_coordinates[3]),
		 (constants.x_coordinates[2],constants.y_coordinates[3]),
		 (constants.x_coordinates[4],constants.y_coordinates[3]),
		 (constants.x_coordinates[6],constants.y_coordinates[3]),
		 (constants.x_coordinates[8],constants.y_coordinates[3])]

# Enumeration type for the pregame settings menu display of the player's pieces
class GuestPreGamePieceDisplay(Enum):
	KING = (constants.x_coordinates[8],constants.y_coordinates[3])
	ADVISOR = (constants.x_coordinates[8],constants.y_coordinates[4])
	ELEPHANT = (constants.x_coordinates[8],constants.y_coordinates[5])
	HORSE = (constants.x_coordinates[8],constants.y_coordinates[6])
	CANNON = (constants.x_coordinates[8],constants.y_coordinates[7])
	CHARIOT = (constants.x_coordinates[8],constants.y_coordinates[8])
	PAWN = (constants.x_coordinates[8],constants.y_coordinates[9])

# Enumeration type for the pregame settings menu display of the player's pieces
class PreGamePieceDisplay(Enum):
	KING = (constants.x_coordinates[0],constants.y_coordinates[3])
	ADVISOR = (constants.x_coordinates[0],constants.y_coordinates[4])
	ELEPHANT = (constants.x_coordinates[0],constants.y_coordinates[5])
	HORSE = (constants.x_coordinates[0],constants.y_coordinates[6])
	CANNON = (constants.x_coordinates[0],constants.y_coordinates[7])
	CHARIOT = (constants.x_coordinates[0],constants.y_coordinates[8])
	PAWN = (constants.x_coordinates[0],constants.y_coordinates[9])

# Class object for the Piece
class Piece():
	# Class initializer
	# INPUT: piece type, where it resides on the board, where its collision rectangle
	#				 is, how many points the piece is worth
	# OUTPUT: Initialized Piece object 
	def __init__(self, piece_type, location, image_location, collision_rect, point_value):
		self.piece_type = piece_type
		self.location = location
		self.image_location = image_location
		self.collision_rect = collision_rect
		self.point_value = point_value
		self.is_clicked = False
		self.image = "Pieces/Blank_Piece.png"