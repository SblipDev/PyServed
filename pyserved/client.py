"""
________________________________
|                              |
| pyserved                     |
|                              |
| Only works with utf-8        | 
| files. (for now.)            |
|                              | 
| By:                          |
| Shaurya Pratap Singh         |
| 2021 ©                       |
|______________________________|
"""

import sys
import socket
import readline
import os

HEADER = 64


class Client:
    def __init__(self, server, port):
        self.SERVER_HOST = server
        self.SERVER_PORT = port
        self.BUFFER_SIZE = 1024 * 100000
        self.SEPARATOR = "<Order66>"
        self.s = socket.socket()
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))

    def listen(self):
        self.s.listen(5)

    def accept(self):
        self.client_socket, self.address = self.s.accept()
        return (self.client_socket, self.address)

    def receive(self):
        received = self.client_socket.recv(self.BUFFER_SIZE).decode()
        filename, filesize = received.split(self.SEPARATOR)
        self.filename = os.path.basename(filename)
        self.filesize = int(filesize)
        return self.filename, self.filesize

    def write(self):
        with open(self.filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = self.client_socket.recv(self.BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)


    def close(self):
        # close the client socket
        self.client_socket.close()
        # close the server socket
        self.s.close()
        

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!q"

def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


SERVER = get_internal_ip()
PORT = 8080
ADDR = (SERVER, PORT)

try:
    if sys.argv[1] is None:
        pass
    else:
        if '-port' in sys.argv[1]:
            PORT = int(sys.argv[2])
            # print(PORT)
            ADDR = (SERVER, PORT)

except IndexError:
    pass

try:
    client = Client(SERVER, PORT)
    print("[SERVER]: Server is running on {}:{}".format(SERVER, PORT))
    print("[SERVER]: Waiting for a connection...")
    client.listen()
    _, address = client.accept()
    print("[SERVER] : Connection at {}:{}".format(address[0], address[1]))
    print("[SERVER] : Waiting for a file...")
    client.receive()
    print("[SERVER] : Received file {}.".format(client.filename))
    client.write()
    print("[SERVER]: File transferred successfully. Closing connection...")
    client.close()
except KeyboardInterrupt:
    print("\n[SERVER]: Keyboard interrupt.")
    client.close()