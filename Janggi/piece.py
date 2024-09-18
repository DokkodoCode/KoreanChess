"""
-----------------------piece.py-----------------------------------
o This file is to hold the data for each piece in Janggi
o Last Modified - September 17th 2024
------------------------------------------------------------------
"""

# libraries
from enum import Enum
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
	KING = [(470,770)]
	ADVISOR = [(373,862),(567,862)]
	ELEPHANT = [(276,862),(761,862)]
	HORSE = [(179,862),(664,862)]
	CANNON = [(179,677),(761,677)]
	CHARIOT = [(82,862),(858,862)]
	PAWN = [(82,586),(276,586),(470,586),(664,586),(858,586)]

# Enumeration type for each opponent's piece's starting position
class OpponentPiecePosition(Enum):
	KING = [(470,128)]
	ADVISOR = [(373,37),(567,37)]
	ELEPHANT = [(276,37),(664,37)]
	HORSE = [(179,37),(761,37)]
	CANNON = [(179,219),(761,219)]
	CHARIOT = [(82,37),(858,37)]
	PAWN = [(82,312),(276,312),(470,312),(664,312),(858,312)]

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