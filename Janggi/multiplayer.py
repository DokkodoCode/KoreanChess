"""
----------------------multiplayer.py-----------------------------
o This file handles networking and data serialization for multiplayer
o Last Modified - April 5, 2025
------------------------------------------------------------------
"""

import socket
import json
from piece import Position
from helper_funcs import reformat_piece_collision
import constants
import pygame
from enum import Enum
import time
import traceback

# Define canonical coordinate system
class Perspective(Enum):
    HOST = "host"  # Host's view 
    CLIENT = "client"  # Client's view

class MessageType(Enum):
    CONNECT = "CONNECT"
    SETTINGS = "SETTINGS"
    SWAP = "SWAP"
    SWAP_DONE = "SWAP_DONE"  
    MOVE = "MOVE"
    SYNC = "SYNC"
    TURN = "TURN"
    PASS = "PASS"
    EXIT = "EXIT"

class GamePhase(Enum):
    CONNECTING = "connecting"
    SETTINGS = "settings"
    HOST_HORSE_SWAP = "host_horse_swap"
    CLIENT_HORSE_SWAP = "client_horse_swap"
    GAMEPLAY = "gameplay"
    GAME_OVER = "game_over"
    CREATE_JOIN_GAME = 'create join game'
    JOIN_GAME = 'join game'
    CREATE_GAME = 'create game'

# -------------------------------------------------------------------------
# Coordinate Transformation Functions
# -------------------------------------------------------------------------

def transform_coordinates(coords, flip_horizontal=False, flip_vertical=False):
    """Transform coordinates based on perspective differences
    
    Args:
        coords: A tuple containing (x, y) coordinates
        flip_horizontal: Whether to flip horizontally (for different perspectives)
        flip_vertical: Whether to flip vertically (for different perspectives)
        
    Returns:
        Transformed (x, y) coordinates as a tuple
    """
    if not coords or len(coords) != 2:
        return coords
        
    x, y = coords
    
    if flip_horizontal:
        # Flip x-coordinate horizontally across the board
        try:
            x_index = constants.x_coordinates.index(x)
            x = constants.x_coordinates[len(constants.x_coordinates) - 1 - x_index]
        except (ValueError, IndexError):
            # Find closest x-coordinate and mirror it
            distances = [(abs(coord - x), i) for i, coord in enumerate(constants.x_coordinates)]
            if distances:
                closest_idx = min(distances)[1]
                mirror_idx = len(constants.x_coordinates) - 1 - closest_idx
                
                # Use the mirrored coordinate plus any offset from the closest match
                offset = x - constants.x_coordinates[closest_idx]
                x = constants.x_coordinates[mirror_idx] - offset
    
    if flip_vertical:
        # Flip y-coordinate vertically across the board
        try:
            y_index = constants.y_coordinates.index(y)
            y = constants.y_coordinates[len(constants.y_coordinates) - 1 - y_index]
        except (ValueError, IndexError):
            # Find closest y-coordinate and mirror it
            distances = [(abs(coord - y), i) for i, coord in enumerate(constants.y_coordinates)]
            if distances:
                closest_idx = min(distances)[1]
                mirror_idx = len(constants.y_coordinates) - 1 - closest_idx
                
                # Use the mirrored coordinate plus any offset from the closest match
                offset = y - constants.y_coordinates[closest_idx]
                y = constants.y_coordinates[mirror_idx] - offset
    
    return (x, y)

def host_to_canonical(coords):
    """Convert host view coordinates to canonical coordinates (identity function)"""
    return coords

def client_to_canonical(coords):
    """Convert client view coordinates to canonical coordinates"""
    return transform_coordinates(coords, flip_horizontal=True, flip_vertical=True)

def canonical_to_host(coords):
    """Convert canonical coordinates to host view coordinates (identity function)"""
    return coords

def canonical_to_client(coords):
    """Convert canonical coordinates to client view coordinates"""
    return transform_coordinates(coords, flip_horizontal=True, flip_vertical=True)

def transform_rect(rect, flip_horizontal=False, flip_vertical=False):
    """Transform rectangle coordinates based on perspective"""
    if not rect:
        return rect
        
    # Transform the topleft coordinate
    new_topleft = transform_coordinates((rect.x, rect.y), 
                                       flip_horizontal=flip_horizontal, 
                                       flip_vertical=flip_vertical)
    
    # Create new rectangle with same size but transformed position
    return pygame.Rect(new_topleft[0], new_topleft[1], rect.width, rect.height)

# -------------------------------------------------------------------------
# Serialization Functions
# -------------------------------------------------------------------------

def serialize_piece_positions(pieces, perspective=Perspective.HOST):
    """Convert a list of piece objects to a serializable format with grid positions"""
    serialized = {}
    
    if not pieces:
        return serialized
        
    for piece in pieces:
        piece_type = piece.piece_type.value
        
        # Get grid position (file, rank)
        file = piece.position.file
        rank = piece.position.rank
        
        # Transform coordinates if client perspective
        if perspective == Perspective.CLIENT:
            file = 8 - file  # Flip horizontally
            rank = 9 - rank  # Flip vertically
        
        # Initialize entry if it doesn't exist
        if piece_type not in serialized:
            serialized[piece_type] = []
            
        # Add piece with unique ID, grid position and pixel data
        serialized[piece_type].append({
            'id': piece.id,  # Include unique ID for reliable matching
            'position': {'file': file, 'rank': rank},
            'location': piece.location,
            'image_location': piece.image_location,
            'collision_rect': {
                'x': piece.collision_rect.x,
                'y': piece.collision_rect.y,
                'width': piece.collision_rect.width,
                'height': piece.collision_rect.height
            }
        })
    
    return serialized

def deserialize_piece_positions(serialized_data, pieces, perspective=Perspective.HOST, protected_pieces=None):
    """Update piece positions from serialized data"""
    if not serialized_data or not pieces:
        return
    
    if protected_pieces is None:
        protected_pieces = {}
    
    role_prefix = "HOST: " if perspective == Perspective.HOST else "CLIENT: "
    
    # Group existing pieces by type and ID for more reliable matching
    piece_by_id = {}
    piece_by_type = {}
    
    for piece in pieces:
        # Map by ID if available
        if hasattr(piece, 'id') and piece.id:
            piece_by_id[piece.id] = piece
        
        # Also group by type as fallback
        piece_type = piece.piece_type.value
        if piece_type not in piece_by_type:
            piece_by_type[piece_type] = []
        piece_by_type[piece_type].append(piece)
    
    # Process each piece type in the serialized data
    for piece_type, positions in serialized_data.items():
        if piece_type in piece_by_type:
            # Track which pieces have been updated
            updated_pieces = set()
            
            # First pass: try to match by ID (most reliable)
            for i, piece_data in enumerate(positions):
                piece_id = piece_data.get('id')
                if piece_id and piece_id in piece_by_id:
                    piece = piece_by_id[piece_id]
                    
                    # Skip protected pieces (recently moved by local player)
                    if piece_id in protected_pieces:
                        print(f"{role_prefix}Skipping update for protected piece: {piece.piece_type.value}")
                        updated_pieces.add(piece)
                        continue
                    
                    # Get grid position from serialized data
                    grid_pos = piece_data.get('position', {})
                    file = grid_pos.get('file', 0)
                    rank = grid_pos.get('rank', 0)
                    
                    # Transform if necessary
                    if perspective == Perspective.CLIENT:
                        file = 8 - file  # Flip horizontally
                        rank = 9 - rank  # Flip vertically
                    
                    # Update piece's grid position
                    piece.position = Position(file, rank)
                    
                    # Update pixel locations for rendering
                    location = constants.x_coordinates[file], constants.y_coordinates[rank]
                    piece.location = location
                    piece.image_location = location
                    
                    # Update collision rectangle
                    piece.collision_rect = reformat_piece_collision(
                        location, piece.collision_rect)
                    
                    updated_pieces.add(piece)
            
            # Second pass: match remaining pieces by index
            type_pieces = [p for p in piece_by_type[piece_type] if p not in updated_pieces]
            remaining_positions = [p for i, p in enumerate(positions) 
                                  if not p.get('id') or p.get('id') not in piece_by_id]
            
            for i, piece_data in enumerate(remaining_positions):
                if i < len(type_pieces):
                    piece = type_pieces[i]
                    
                    # Skip protected pieces (recently moved by local player)
                    piece_id = piece.id if hasattr(piece, 'id') else None
                    if piece_id in protected_pieces:
                        print(f"{role_prefix}Skipping update for protected piece: {piece.piece_type.value}")
                        continue
                    
                    # Get grid position from serialized data
                    grid_pos = piece_data.get('position', {})
                    file = grid_pos.get('file', 0)
                    rank = grid_pos.get('rank', 0)
                    
                    # Transform if necessary
                    if perspective == Perspective.CLIENT:
                        file = 8 - file  # Flip horizontally
                        rank = 9 - rank  # Flip vertically
                    
                    # Update piece's grid position
                    piece.position = Position(file, rank)
                    
                    # Update pixel locations for rendering
                    location = constants.x_coordinates[file], constants.y_coordinates[rank]
                    piece.location = location
                    piece.image_location = location
                    
                    # Update collision rectangle
                    piece.collision_rect = reformat_piece_collision(
                        location, piece.collision_rect)

def serialize_move(piece_type, from_pos, to_pos, perspective=Perspective.HOST):
    """Create a serialized move message using grid coordinates"""
    # Get grid coordinates
    from_file, from_rank = from_pos.position.file, from_pos.position.rank
    to_file, to_rank = to_pos.position.file, to_pos.position.rank
    
    # Transform if from client perspective
    if perspective == Perspective.CLIENT:
        from_file, from_rank = 8 - from_file, 9 - from_rank
        to_file, to_rank = 8 - to_file, 9 - to_rank
    
    return {
        'piece_type': piece_type,
        'from_pos': {'file': from_file, 'rank': from_rank},
        'to_pos': {'file': to_file, 'rank': to_rank}
    }


def serialize_board_state(host_pieces, guest_pieces, perspective=Perspective.HOST):
    """Create a full board state serialization including both players' pieces
    
    Args:
        host_pieces: List of host player's pieces
        guest_pieces: List of guest player's pieces
        perspective: The perspective to serialize from (HOST or CLIENT)
        
    Returns:
        Serialized board state as a dictionary
    """
    # Serialize both players' pieces to canonical format
    host_data = serialize_piece_positions(host_pieces, perspective)
    guest_data = serialize_piece_positions(guest_pieces, perspective)
    
    # Create the complete board state
    board_state = {
        'host': host_data,
        'guest': guest_data
    }
    
    return board_state

# -------------------------------------------------------------------------
# Socket Connection Classes
# -------------------------------------------------------------------------

class SocketConnection:
    """Base class for socket connections"""
    
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.sock = None
        self.buffer = ""  # Buffer for incomplete messages

    def create_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print(f"Socket created successfully")
            return True
        except Exception as e:
            print(f"Error creating socket: {e}")
            return False

    def close(self):
        if self.sock:
            try:
                self.sock.close()
                print("Socket closed")
                return True
            except Exception as e:
                print(f"Error closing socket: {e}")
                return False
        return True

    def send(self, message):
        """Send a message as JSON with newline delimiter"""
        try:
            # Ensure the message ends with newline for message delimiting
            if isinstance(message, dict):
                message = json.dumps(message)
                
            if not message.endswith("\n"):
                message += "\n"
                
            message_bytes = message.encode()
            self.sock.sendall(message_bytes)
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    def receive(self, bytes=1024):
        """Receive a message with newline delimiter"""
        try:
            # Try to receive data
            data = self.sock.recv(bytes)
            if not data:
                # Connection closed by remote side
                print("Connection closed by remote side")
                return None
                
            # Decode and add to buffer
            decoded_data = data.decode()
            self.buffer += decoded_data
            
            # Look for complete message (delimited by newline)
            if "\n" in self.buffer:
                message, self.buffer = self.buffer.split("\n", 1)
                return message
            else:
                # No complete message yet
                return None
                
        except BlockingIOError:
            # No data available in non-blocking mode
            return None
        except ConnectionResetError:
            print("Connection was reset by peer")
            return None
        except Exception as e:
            print(f"Error receiving message: {e}")
            traceback.print_exc()
            return None

    def set_non_blocking(self, non_blocking=True):
        """Set the socket to non-blocking mode"""
        if self.sock:
            self.sock.setblocking(not non_blocking)


class Server(SocketConnection):
    """Server class for hosting the game"""
    
    def __init__(self, host, port):
        super().__init__(host, port)
        self.client_sock = None
        self.addr = None

    def bind_socket(self):
        try:
            self.sock.bind((self.HOST, self.PORT))
            print(f"Server bound to {self.HOST}:{self.PORT}")
        except Exception as e:
            print(f"Error binding socket: {e}")
            raise e

    def listen(self, backlog=1):
        try:
            self.sock.listen(backlog)
            print(f"Server listening with backlog {backlog}")
        except Exception as e:
            print(f"Error listening: {e}")
            raise e

    def accept_client(self, timeout=60):
        try:
            if timeout:
                self.sock.settimeout(timeout)
                
            self.client_sock, self.addr = self.sock.accept()
            print(f"Accepted client connection from {self.addr}")
            
            # if timeout:
            #     self.sock.settimeout(None)  # Reset timeout
                
        except socket.timeout:
            print("Accept timed out, no client connected")
            raise e
        except Exception as e:
            print(f"Error accepting client: {e}")
            raise e
        
    def send(self, message):
        """Send a message to the connected client"""
        try:
            if self.client_sock:
                # Ensure the message ends with newline for message delimiting
                if isinstance(message, dict):
                    message = json.dumps(message)
                    
                if not message.endswith("\n"):
                    message += "\n"
                    
                message_bytes = message.encode()
                self.client_sock.sendall(message_bytes)
                return True
            else:
                print("No client connected")
                return False
        except Exception as e:
            print(f"Error sending message to client: {e}")
            traceback.print_exc()
            return False

    def receive(self, bytes=1024):
        """Receive a message from the connected client"""
        try:
            if self.client_sock:
                # Try to receive data
                data = self.client_sock.recv(bytes)
                if not data:
                    # Connection closed by remote side
                    print("Client connection closed")
                    return None
                    
                # Decode and add to buffer
                decoded_data = data.decode()
                self.buffer += decoded_data
                
                # Look for complete message (delimited by newline)
                if "\n" in self.buffer:
                    message, self.buffer = self.buffer.split("\n", 1)
                    return message
                else:
                    # No complete message yet
                    return None
            else:
                print("No client connected")
                return None
                
        except BlockingIOError:
            # No data available in non-blocking mode
            return None
        except ConnectionResetError:
            print("Connection with client was reset")
            return None
        except Exception as e:
            print(f"Error receiving message from client: {e}")
            traceback.print_exc()
            return None

    def set_client_non_blocking(self, non_blocking=True):
        """Set the client socket to non-blocking mode"""
        if self.client_sock:
            self.client_sock.setblocking(not non_blocking)


class Client(SocketConnection):
    """Client class for connecting to the game server"""
    
    def __init__(self, host, port):
        super().__init__(host, port)

    def connect(self, timeout=5):
        try:
            self.create_socket()
            
            if timeout:
                self.sock.settimeout(timeout)
                
            self.sock.connect((self.HOST, self.PORT))
            print(f"Connected to server at {self.HOST}:{self.PORT}")
            
            if timeout:
                self.sock.settimeout(None)  # Reset timeout
                
            return True
        except socket.timeout:
            print(f"Connection attempt timed out after {timeout} seconds")
            raise TimeoutError
        except ConnectionRefusedError:
            print("Connection refused. Is the server running?")
            raise ConnectionRefusedError
        except Exception as e:
            print(f"Error connecting to server: {e}")
            traceback.print_exc()
            return Exception