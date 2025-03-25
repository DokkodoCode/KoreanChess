# MULTIPLAYER.py

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

def start_server(host, port):
    # set up server
    server = Server(host, port)
    server.create_socket()
    server.bind_socket()
    server.listen()

    # Accept client
    client_sock = server.accept_client()
    print("accepted connection")

    # repeat 
    while True:
        msg = server.receive()
        if msg == 'exit':
            server.close()
            break
        else:
            print("message received:", msg)
            server.send(msg)

def start_client(host, port):
    # set up client
    tcp = Client(host, port)
    tcp.create_socket()
    tcp.connect()

    while True:
        msg = input("enter a message to send ('exit' to exit): ")
        tcp.send(msg)

        if msg == 'exit':
            tcp.close()
            break

if __name__ == "__main__":
    option = input("Would you like to be a host(1), or a client(2): ")
    host, port = socket.gethostbyname(socket.gethostname()), 5000
    print(f"Enter this on the other computer: {host}")

    match option:
        case "1":
            # become a host
            start_server(host, port)

        case "2":
            # become a clinet
            host = input("enter the host ip: ")
            start_client(host, port)

        case _:
            print("not a valid option")
            exit(1)
