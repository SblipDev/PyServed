#!/usr/bin/env python

"""
deepthought@42 ~ $ pdlisten

[{constants.success}]: Server is listening on 192.168.1.58:8080
[{constants.success}]: Connection Key: 192@168@1@58+8080
[{constants.success}]: Waiting for a connection for files...

This program is used to listen for incoming connections from the 
pdsnd.py program. If it recieves a connection, it will write the
file in the directory. 

The pdsnd command is used for sending a file to the server
created by the server "pdlisten" program.

### PDLISTEN ###

The pdlisten command when run gives a connection key which 
is needed to send a file while using pdsnd.

The -port argument may be used to change the port of the server.

Thanks for having interest in this library.
This file is the script for the pdlisten program.
"""

# Import libraries

import sys
import socket
import readline
import os
import constants
from rich import print

# Decodes the key


def keymaker(key: str) -> str:
    return key.replace(".", "@").replace(":", "+")


# HEADER Variable
HEADER = 64

# CLIENT
# A class which makes life easier.
class Client:
    def __init__(self, server, port):

        # CHANGE STUFF HERE
        self.SERVER_HOST = server
        self.SERVER_PORT = port
        # CHANGE STUFF HERE

        self.BUFFER_SIZE = 4096
        self.SEPARATOR = "<pyserved21>"
        self.s = socket.socket()
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))

    def listen(self):
        # Listen for incoming connections
        self.s.listen(10)

    def accept(self):
        # Accept incoming connections from client
        # and return client socket and address.
        self.client_socket, self.address = self.s.accept()
        return (self.client_socket, self.address)

    def receive(self):
        # Receive message from client_socket
        # and return filename and filesize
        received = self.client_socket.recv(self.BUFFER_SIZE).decode()
        filename, filesize = received.split(self.SEPARATOR)
        self.filename = os.path.basename(filename)
        self.filesize = int(filesize)
        return self.filename, self.filesize

    def write(self):
        # Write file which is received from client_socket
        # in the same directory.
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


# Function to get Internal IP of device


def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


# CHANGE SERVER HERE
SERVER = get_internal_ip()
# CHANGE SERVER HERE

# CHANGE PORT HERE
PORT = 8080
# CHANGE PORT HERE

ADDR = (SERVER, PORT)

# Check if port is not in use
# If port is in use, return True
# Else False
def is_port_in_use() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((get_internal_ip(), PORT)) == 0


# Checks if -port argument is passed
try:
    if sys.argv[1] is None:
        pass
    else:
        if "-port" in sys.argv[1]:
            PORT = int(sys.argv[2])
            # print(PORT)
            ADDR = (SERVER, PORT)
except IndexError:
    pass

# If port 8080 is in use,
# End program with message informing that port is in use
if is_port_in_use() is True:
    print(
        f"[bold red][{constants.error}]: Port 8080 is already in use in your network. Choose another port instead using the '-port' parameter.[/]"
    )
    exit()

# Start server

try:
    client = Client(SERVER, PORT)

    print(
        f"[bold green][{constants.success}]:[/] Server is listening on {SERVER}:{PORT}"
    )
    print(
        f"[bold green][{constants.success}]:[/] Connection Key: {keymaker(str(SERVER + ':' + str(PORT)))}"
    )
    print(
        f"[bold green][{constants.success}]:[/] Waiting for a connection for files..."
    )

    client.listen()
    _, address = client.accept()

    print(
        f"[bold green][{constants.success}]:[/] Connection from {address[0]}:{address[1]} accepted."
    )
    print(f"[bold green][{constants.success}]:[/] Reading file data.....")

    try:
        client.receive()
    except ValueError as e:
        print(
            f"{repr(e)} \n\n [bold red][{constants.error}]: An error occured. Please try again in few seconds....[/]"
        )
        exit()

    print(
        f"[bold green][{constants.success}]:[/] Received file '[bold yellow]{client.filename}[/]', saving to current directory."
    )
    client.write()

    print(
        "[bold green][{constants.success}]:[/] File transferred successfully. Closing connection..."
    )
    client.close()

except KeyboardInterrupt:
    print(f"\n\n[bold red][{constants.error}]: KeyboardInterrupt[/]")
    exit()

except Exception as e:
    print(
        f"\n\n[bold red][{constants.error}]: {repr(e)} \n\n If the problem persists, contact the owner of the package at https://github.com/SblipDev/pyserved[/] \n"
    )
    exit()
