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

    Loop:
        - client recieves packet
        - unpack packet
        - get FEN string from packet
        - client makes a move
        - create new FEN string after client has made a move
        - send to server

'''

import socket


class SocketConnection:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.sock = None

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        self.sock.close()

    def send(self, message):
        try:
            self.sock.sendall(message.encode())
        
        except Exception as err:
            print("sending message unsucessful:", err)

    def receive(self, bytes=1024):
        try:
            return self.sock.recv(bytes).decode()
        
        except UnicodeDecodeError:
            print("Couldnt decode message recved.")
            
        except TimeoutError:
            print("message wasnt receieved")


class Server(SocketConnection):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.client_sock = None
        self.addr = None

    def bind_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))

    def listen(self):
        self.sock.listen()

    def accept_client(self):
        self.client_sock, self.addr = self.sock.accept()
        print(f"accepted client connection {self.addr[1]}")
        return self.client_sock
        
    def send(self, message):
        try:
            if self.client_sock:
                self.client_sock.sendall(message.encode())
            else:
                print("No client connected")
        except Exception as err:
            print("sending message unsuccessful:", err)

    def receive(self, bytes=1024):
        try:
            if self.client_sock:
                return self.client_sock.recv(bytes).decode()
            else:
                print("No client connected")
                return None
        except UnicodeDecodeError:
            print("Couldn't decode message received.")
        except TimeoutError:
            print("message wasn't received")
        except Exception as err:
            print("Error receiving:", err)

class Client(SocketConnection):
    
    def __init__(self, host, port):
        super().__init__(host, port)

    def connect(self):
        try:
            self.create_socket()
            self.sock.connect((self.HOST, self.PORT))

        except ConnectionRefusedError:
            print("Connection not successful")
            exit(1)