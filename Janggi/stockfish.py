"""
---------------------------stockfish.py---------------------------
o This file is to hold logic for the ai engine (fairy-stockfish)
o Last Modified - November 19th 2024
------------------------------------------------------------------
"""

# python imports
import subprocess
import os

os_name = os.name
EXECUTABLE_PATH = ""
if (os_name == "posix"):
    EXECUTABLE_PATH = "./stockfish"
elif (os_name == 'nt'):
    EXECUTABLE_PATH = "./fairy-stockfish-largeboard_x86-64"
else: 
    print("SOMETHING HAS GONE WRONG")

# Start the engine process
# Formality stuff
engine = subprocess.Popen(
    [EXECUTABLE_PATH],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Function for sending commands to the engine.
def send_command(command):
    engine.stdin.write(command + '\n')
    engine.stdin.flush()

# Initialize UCI mode and set the variant to Janggi.
# This is just formality stuff
send_command("uci")
send_command("setoption name UCI_Variant value janggi")
send_command("position startpos")

# Function to generate FEN string from the board state
# The FEN string is a way of recording the current board state in string format.
# This string format is what is passed to stockfish so that it can make a move.
def generate_fen(board, active_player):
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
    fen_string = "/".join(fen_rows) + " " + active_player
    return fen_string

# Example board state
# We need to import the current board state and convert it into this format.
janggi_board = [
    ["r", "n", "b", "a", "k", "a", "b", "n", "r"],
    [".", "c", ".", ".", ".", ".", ".", "c", "."],
    ["p", ".", "p", ".", "p", ".", "p", ".", "p"],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    ["P", ".", "P", ".", "P", ".", "P", ".", "P"],
    [".", "C", ".", ".", ".", ".", ".", "C", "."],
    ["R", "N", "B", "A", "K", "A", "B", "N", "R"],
]
# w means white in chess terms, in this case w = red.
# b meand black in chess terms, in this case b = blue
# This should be set to the opposite of what was chosen in the start
# menu by the player.
active_player = "w"

# Generate and send FEN string for the current board state
current_fen = generate_fen(janggi_board, active_player)
send_command(f"position fen {current_fen}")

# Function to get the best move from the engine.
# The engine will output several lines. This searches the lines
# to find the one labeled "bestmove", which we will use to update the board.
# Best move will come out in a coordinate format similar to chess. eg. i3h3. 
# which means move the piece at coordinate i3 to h3.
def get_engine_move():
    while True:
        output = engine.stdout.readline().strip()
        if "bestmove" in output:
            best_move = output.split()[1]
            return best_move

# Ask the engine to make a move (easy difficulty - depth 1)
# Difficulty can be adjusted by changing the depth at which the engine searches
# for a move, as shown here, or by limiting its thinking time.
send_command("go depth 1")

# Retrieve the engine's move
try:
    best_move = get_engine_move()
    print(f"Engine's move: {best_move}")
except Exception as e:
    print(f"Error retrieving move: {e}")

# Quit the engine
send_command("quit")
