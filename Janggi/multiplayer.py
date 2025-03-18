import socket
PORT = 5000

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

    def bind_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))

    def listen(self):
        self.sock.listen()

    def accept_client(self):
        self.sock, self.addr = self.sock.accept()
        print(f"accepted client connection {self.addr[1]}")
        return self.sock

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
    host = socket.gethostbyname(socket.gethostname())
    option = input("Would you like to be a host(1), or a client(2): ")

    match option:
        case "1":
            start_server(host, PORT)

        case "2":
            start_client(host, PORT)

        case _:
            print("not a valid option")
