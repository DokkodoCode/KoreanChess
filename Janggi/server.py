"""
----------------------server.py-----------------------------------
o This file is not used and may be used for future development
o Last Modified - N/A
------------------------------------------------------------------
"""

"""# Dependencies
import socket
from _thread import *
import sys


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: # Attempt to bind the server to the port
    s.bind((server,port))
except socket.error as e: # Return a message if there is an error with binding the server
    str(e)

s.listen(2) # Open the port and listen for any client connections (maximum of two player connection)
print("Waiting for an opponent...")

def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending:", reply)
            conn.sendall(str.encode(reply))
        except:
            break
    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept() # Accept any connection
    print("Connected to:", addr)

    start_new_thread(threaded_client,(conn,)) # Start a thread with the connection"""