'''
MULTIPLAYER.PY


So, what's the game plan?

One player will be a Host, and the other will be the client that connects to the host

What does the host need to do?
    1. create a socket
    2. create a password
    3. listen for and accept client
    4. initialize game

What does the client need to do?
    1. enter a code
    2. connect to host

Communication protocol is message-based with formats:
- "SETTINGS:|<color>|<piece_convention>" - Send initial game settings
- "SWAP:|<side>|<piece1>|<piece2>" - Send horse swap (side can be "left" or "right")
- "PASS" - Signal turn passing
- "MOVE:|<pieceType>|<fromPos>|<toPos>" - Send move information
- "SYNC:|<serialized_pieces>" - Send full board state
- "EXIT" - Signal game ending

'''

import socket
import json

class SocketConnection:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.sock = None
        self.buffer = ""  # Buffer for incomplete messages

    def create_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except Exception as e:
            print(f"Error creating socket: {e}")

    def close(self):
        if self.sock:
            try:
                self.sock.close()
                print("Socket closed")
            except Exception as e:
                print(f"Error closing socket: {e}")

    def send(self, message):
        """Send a message to the connected socket"""
        try:
            if not message.endswith("\n"):
                message += "\n"  # Add newline as message delimiter
            message_bytes = message.encode()
            self.sock.sendall(message_bytes)
            print(f"Sent {len(message_bytes)} bytes: {message.strip()}")
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    def receive(self, bytes=1024):
        """Receive a message from the connected socket"""
        try:
            # Try to receive data
            data = self.sock.recv(bytes)
            if not data:
                # Connection closed by remote side
                return None
                
            # Decode and add to buffer
            decoded_data = data.decode()
            self.buffer += decoded_data
            print(f"Received raw data: {decoded_data}")
            
            # Look for complete message (delimited by newline)
            if "\n" in self.buffer:
                message, self.buffer = self.buffer.split("\n", 1)
                print(f"Extracted message: {message}")
                return message
            else:
                # No complete message yet
                return None
                
        except BlockingIOError:
            # No data available (non-blocking socket)
            return None
        except ConnectionResetError:
            print("Connection was reset by peer")
            return None
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None

    def set_non_blocking(self, non_blocking=True):
        """Set the socket to non-blocking mode"""
        if self.sock:
            self.sock.setblocking(not non_blocking)


class Server(SocketConnection):
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

    def listen(self):
        try:
            self.sock.listen(1)
            print("Server listening for connections")
        except Exception as e:
            print(f"Error listening: {e}")

    def accept_client(self):
        try:
            self.client_sock, self.addr = self.sock.accept()
            print(f"Accepted client connection from {self.addr}")
            return self.client_sock
        except Exception as e:
            print(f"Error accepting client: {e}")
            return None
        
    def send(self, message):
        """Send a message to the connected client socket"""
        try:
            if self.client_sock:
                if not message.endswith("\n"):
                    message += "\n"  # Add newline as message delimiter
                message_bytes = message.encode()
                self.client_sock.sendall(message_bytes)
                print(f"Sent to client {len(message_bytes)} bytes: {message.strip()}")
                return True
            else:
                print("No client connected")
                return False
        except Exception as e:
            print(f"Error sending message to client: {e}")
            return False

    def receive(self, bytes=1024):
        """Receive a message from the connected client socket"""
        try:
            if self.client_sock:
                # Try to receive data
                data = self.client_sock.recv(bytes)
                if not data:
                    # Connection closed by remote side
                    return None
                    
                # Decode and add to buffer
                decoded_data = data.decode()
                self.buffer += decoded_data
                print(f"Received from client raw data: {decoded_data}")
                
                # Look for complete message (delimited by newline)
                if "\n" in self.buffer:
                    message, self.buffer = self.buffer.split("\n", 1)
                    print(f"Extracted client message: {message}")
                    return message
                else:
                    # No complete message yet
                    return None
            else:
                print("No client connected")
                return None
        except BlockingIOError:
            # No data available (non-blocking socket)
            return None
        except ConnectionResetError:
            print("Connection with client was reset")
            return None
        except Exception as e:
            print(f"Error receiving message from client: {e}")
            return None

    def set_client_non_blocking(self, non_blocking=True):
        """Set the client socket to non-blocking mode"""
        if self.client_sock:
            self.client_sock.setblocking(not non_blocking)


class Client(SocketConnection):
    def __init__(self, host, port):
        super().__init__(host, port)

    def connect(self):
        try:
            self.create_socket()
            self.sock.connect((self.HOST, self.PORT))
            print(f"Connected to server at {self.HOST}:{self.PORT}")
            return True
        except ConnectionRefusedError:
            print("Connection refused. Is the server running?")
            return False
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return False

# Helper functions for game state serialization

def serialize_piece_positions(pieces):
    """Convert a list of piece objects to a serializable format"""
    serialized = {}
    for piece in pieces:
        piece_type = piece.piece_type.value
        location = piece.location
        
        # Initialize entry if it doesn't exist
        if piece_type not in serialized:
            serialized[piece_type] = []
            
        # Add piece location
        serialized[piece_type].append({
            'location': location,
            'image_location': piece.image_location,
            'collision_rect': {
                'x': piece.collision_rect.x,
                'y': piece.collision_rect.y,
                'width': piece.collision_rect.width,
                'height': piece.collision_rect.height
            }
        })
    
    return serialized

def deserialize_piece_positions(serialized_data, pieces):
    """Update piece positions from serialized data"""
    if not serialized_data:
        return
        
    # Group pieces by type
    piece_map = {}
    for piece in pieces:
        piece_type = piece.piece_type.value
        if piece_type not in piece_map:
            piece_map[piece_type] = []
        piece_map[piece_type].append(piece)
    
    # Update pieces from serialized data
    for piece_type, positions in serialized_data.items():
        if piece_type in piece_map and len(piece_map[piece_type]) == len(positions):
            # Update each piece of this type
            for i, piece_data in enumerate(positions):
                piece_map[piece_type][i].location = piece_data['location']
                piece_map[piece_type][i].image_location = piece_data['image_location']
                rect_data = piece_data['collision_rect']
                piece_map[piece_type][i].collision_rect.x = rect_data['x']
                piece_map[piece_type][i].collision_rect.y = rect_data['y']
                piece_map[piece_type][i].collision_rect.width = rect_data['width']
                piece_map[piece_type][i].collision_rect.height = rect_data['height']

def serialize_move(piece, from_pos, to_pos):
    """Create a serialized move message with more detailed info"""
    move_data = {
        'piece_type': piece.piece_type.value,
        'from_pos': from_pos,
        'to_pos': to_pos,
    }
    import json
    return f"MOVE:|{json.dumps(move_data)}"

def serialize_swap(side, piece1, piece2):
    """Create a serialized swap message with detailed piece info"""
    swap_data = {
        'side': side,
        'piece1': {
            'type': piece1.piece_type.value,
            'location': piece1.location
        },
        'piece2': {
            'type': piece2.piece_type.value,
            'location': piece2.location
        }
    }
    import json
    return f"SWAP:|{json.dumps(swap_data)}"

def serialize_board_sync(host_pieces, guest_pieces):
    """Create a full board sync message with all pieces"""
    try:
        host_data = serialize_piece_positions(host_pieces)
        guest_data = serialize_piece_positions(guest_pieces)
        
        sync_data = {
            'host': host_data,
            'guest': guest_data
        }
        
        import json
        json_str = json.dumps(sync_data)
        
        # Check if the JSON string is valid
        if not json_str or json_str.isspace():
            print("Warning: Generated empty JSON string for sync")
            return "SYNC:{}"  
            
        # Return without the pipe character for consistency
        return f"SYNC:{json_str}"  
        
    except Exception as e:
        print(f"Error serializing board sync: {e}")
        import traceback
        traceback.print_exc()
        return "SYNC:{}"  # Return a valid but empty JSON object as fallback

def serialize_turn_info(active_player_color, condition=None):
    """Create a serialized turn info message"""
    turn_data = {
        'active_player': active_player_color,
        'condition': condition if condition else "None"
    }
    import json
    return f"TURN:|{json.dumps(turn_data)}"