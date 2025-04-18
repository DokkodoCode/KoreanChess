"""
---------------------------stockfish.py---------------------------
o This file is to hold logic for the ai engine (fairy-stockfish)
o Last Modified - November 19th 2024
------------------------------------------------------------------
"""

import subprocess
import time
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
send_command("uci")
send_command("setoption name UCI_Variant value janggi")
send_command("position startpos")

# Set the difficulty of the engine
def set_difficulty(difficulty="easy"):
    # Send the appropriate skill level and depth based on difficulty

    send_command("setoption name Ponder true")
    send_command("setoption name UCI_LimitStrength true") # Enables poor play from the AI

    if difficulty == "easy":
        send_command("setoption name UCI_Elo value 700")  # Easy difficulty
        send_command("go depth 1")
    elif difficulty == "medium":
        send_command("setoption name UCI_Elo value 1400")# Medium difficulty
        send_command("go depth 5")
    elif difficulty == "hard":
        send_command("setoption name UCI_Elo value 2850")  # Hard difficulty
        send_command("go depth 20")

    # Allow the engine to process the options set
    time.sleep(1)  # Small delay to ensure options are set before moving on

# Function to generate FEN string from the board state
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
# b means black in chess terms, in this case b = blue
active_player = "w"

# Generate and send FEN string for the current board state
current_fen = generate_fen(janggi_board, active_player)
send_command(f"position fen {current_fen}")

# Function to get the best move from the engine.
def get_engine_move(timeout=5):
    start_time = time.time()
    while True:
        output = engine.stdout.readline().strip()
        print(f"Stockfish output: {output}")  # Debugging line
        if "bestmove" in output:
            best_move = output.split()[1]
            return best_move
        if time.time() - start_time > timeout:
            raise TimeoutError("Engine did not return a bestmove in time.")

# Set AI difficulty (adjust as needed)
set_difficulty("medium")  # This should now work based on the difficulty

# Retrieve the engine's move
try:
    best_move = get_engine_move()
    print(f"Engine's move: {best_move}")
except Exception as e:
    print(f"Error retrieving move: {e}")

# Quit the engine
send_command("quit")
