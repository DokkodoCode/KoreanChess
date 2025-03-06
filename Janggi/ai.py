"""
----------------------------ai.py---------------------------------
o This file is to hold logic for the ai
o Last Modified - November 19th 2024
------------------------------------------------------------------
"""

# python imports
import numpy as np
import pygame
import subprocess
from piece import Piece, PieceCollisionSize, PieceType, OpponentPiecePosition
from helper_funcs import reformat_piece_collision
import os 

os_name = os.name
EXECUTABLE_PATH = ""
if (os_name == "posix"):
    EXECUTABLE_PATH = "./stockfish"
elif (os_name == 'nt'):
    EXECUTABLE_PATH = "./fairy-stockfish-largeboard_x86-64"
else: 
    print("SOMETHING HAS GONE WRONG")

class OpponentAI:
    def __init__(self, is_host=False, board_perspective="Top", difficulty="easy", color="Han"):
        self.difficulty = difficulty
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

        # Start the engine process
        self.engine = subprocess.Popen(
            [EXECUTABLE_PATH],
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
        self.send_command("uci")
        self.send_command("setoption name UCI_Variant value janggi")
        self.send_command("position startpos")

        # Apply difficulty settings
        self.set_difficulty(self.difficulty)

    def set_difficulty(self, difficulty):
        """
        Adjust the difficulty of the AI by modifying the engine's skill level or search depth.
        """
        if difficulty == "easy":
            self.send_command("setoption name Skill_Level value 1")  # Lowest skill level
            self.send_command("setoption name UCI_EnginesearchDepth value 5")  # Shallow search depth
        elif difficulty == "medium":
            self.send_command("setoption name Skill_Level value 4")  # Medium skill level
            self.send_command("setoption name UCI_EnginesearchDepth value 10")  # Moderate search depth
        elif difficulty == "hard":
            self.send_command("setoption name Skill_Level value 20")  # Highest skill level
            self.send_command("setoption name UCI_EnginesearchDepth value 20")  # Deep search depth
        else:
            raise ValueError(f"Unsupported difficulty level: {difficulty}")

    def restart_engine(self):
        """
        Restart the engine and apply the difficulty setting again.
        """
        self.engine.terminate()
        self.engine = subprocess.Popen(
            [EXECUTABLE_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        self.send_command("uci")
        self.send_command("setoption name UCI_Variant value janggi")
        self.send_command("position startpos")

        # Reapply the difficulty after restart
        self.set_difficulty(self.difficulty)

    def get_engine_move(self):
        """
        Function to get the best move from the engine based on the difficulty level set.
        """
        while True:
            output = self.engine.stdout.readline().strip()
            if "bestmove" in output:
                best_move = output.split()[1]
                return best_move

    def fill_pieces(self):
        pieces = []  # store the piece objects

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

    def send_command(self, command):
        self.engine.stdin.write(command + '\n')
        self.engine.stdin.flush()

    def flush_engine_output(self):
        import time
        buffer = []
        start_time = time.time()

        while True:
            # Read a line from Stockfish's stdout
            line = self.engine.stdout.readline().strip()
            if line:  # If there's output, store it in the buffer
                buffer.append(line)
            else:
                # If no output and we have waited long enough, break
                if time.time() - start_time > 0.5:  # Avoid hanging indefinitely
                    break

        return buffer

    def notation_to_coordinates(self, location):
        # Define column mappings for Janggi notation
        columns = {'i': 0, 'h': 1, 'g': 2, 'f': 3, 'e': 4, 'd': 5, 'c': 6, 'b': 7, 'a': 8}

        # Get map index value
        column = columns[location[:1]]
        row = int(location[1:]) - 1  # Convert "1" to index 0, etc.

        return (column, row)

    def find_piece_on_board(self, player, board, location):
        for rank, row in enumerate(board.coordinates):
            for file, spot in enumerate(row):
                if (rank, file) == location:
                    for piece in self.pieces:
                        if piece.location == spot:
                            return piece
        return

    def convert_board(self, board, player):
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
            [".", ".", ".", ".", ".", ".", ".", ".", "."]])

        piece_type_mapping = {
            "Chariot": "R",
            "Elephant": "E",
            "Horse": "H",
            "Pawn": "P",
            "King": "K",
            "Advisor": "A",
            "Cannon": "C"
        }

        new_board = self.add_player_pieces(new_board, player, board, piece_type_mapping)
        new_board = self.add_opponent_pieces(new_board, board, piece_type_mapping)
        new_board = np.flipud(new_board)
        new_board = np.fliplr(new_board)
        return new_board

    def add_player_pieces(self, new_board, player, board, piece_type_mapping):
        for row in range(len(board.coordinates)):
            for column in range(len(board.coordinates[row])):
                for piece in player.pieces:
                    if board.coordinates[row][column] == piece.location:
                        new_board[column][row] = piece_type_mapping.get(piece.piece_type.value).lower()
        return new_board

    def add_opponent_pieces(self, new_board, board, piece_type_mapping):
        for row in range(len(board.coordinates)):
            for column in range(len(board.coordinates[row])):
                for piece in self.pieces:
                    if board.coordinates[row][column] == piece.location:
                        new_board[column][row] = piece_type_mapping.get(piece.piece_type.value)
        return new_board

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


