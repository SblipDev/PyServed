"""
deepthought@42 ~ $ pdlisten

[SERVER] : Program Initialized at directory './'
[SERVER] : Enter Connection Key : 192@168@1@58+8080
[SERVER] : Set server ip to 192.168.1.58:8080
[SERVER] : Filename: file.txt

This program is used to listen for incoming connections from the 
pdsnd.py program. If it recieves a connection, it will write the
file in the directory. 

The pdsnd command is used for sending a file to the server
created by the server.

### PDSND ###

The pdlisten command when run asks for the path of the file you
want to send and the connection key provided by the pdlisten 
program.

The -port argument may be used to change the port of the server.

Thanks for having interest in this library.
"""

# Import Libraries

import socket
import os
import readline
import sys

from rich import print
from rich.prompt import Prompt

# Variables

SEPARATOR = "<py42/>"
BUFFER_SIZE = 1024 * 100000

# Function for sending file


def send_file(filename, host, port):
    filesize = os.path.getsize(filename)
    s = socket.socket()
    s.connect((host, int(port)))

    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)

    s.close()

    return True


# Function for getting internal ip


def get_internal_ip():
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss.connect(("8.8.8.8", 80))
    ip = ss.getsockname()[0]
    ss.close()
    return ip


# CHANGE SAVE DIRECTORY (manually)  HERE
SAVE_DIR = "./"
# CHANGE SAVE DIRECTORY (manually)  HERE

# CHANGE HOST (manually)  HERE
SERVER = str(get_internal_ip())
# CHANGE HOST (manually)  HERE

# CHANGE PORT (manually)  HERE
PORT = 8080
# CHANGE PORT (manually) HERE

ADDR = (SERVER, PORT)

# Checks if port argument is passed
try:
    if sys.argv[1] is None:
        pass
    else:
        # Sets PORT Variable to argument passed
        if "-port" in sys.argv[1]:
            PORT = int(sys.argv[2])
            # print(PORT)
            ADDR = (SERVER, PORT)
# Ignore Error which comes with no arguments being
# passed.
except IndexError:
    pass

# Creates the key

keybreaker = lambda key: key.replace("@", ".").replace("+", ":").strip(":")

# Program start

try:
    print(
        "[bold green][SERVER][/] : Program Initialized at directory '{}'".format(
            SAVE_DIR
        )
    )

    # Connection key prompt
    connectionkey = Prompt.ask("[bold green][SERVER][/] : Enter Connection Key ")

    try:
        SERVER, PORT = tuple(keybreaker(connectionkey).split(":"))
    except ValueError:
        print(
            f"\n[bold red]Invalid Connection key {connectionkey}. Please check if your connection key is valid.[/]"
        )
        exit()

    print(
        "[bold green][SERVER][/] : Set server ip to {}".format(
            keybreaker(connectionkey)
        )
    )

    # Prompts for file path
    filename = Prompt.ask("[bold green][SERVER][/] : Filename")

    # Send function.
    send_file(filename, SERVER, PORT)

    # Prints success message
    print("[bold green][SERVER][/] : Got file path successfully.")
    print(
        f"[bold green][SERVER][/] : Sending [bold yellow]{filename}[/] to {SERVER}:{PORT}"
    )
    print(f"[bold green][SERVER][/] : Sent file. :)")
except KeyboardInterrupt:
    # KeyboardInterrupt Error Handling
    print("\n[bold red]KeyboardInterrupt :([/]")
    exit()
except ConnectionRefusedError:
    # ConnectionRefusedError Error Handling
    print(f"\n[bold red]Connection Refused. Please check the server program.[/]")
    exit()
except FileNotFoundError:
    # FileNotFoundError Error Handling
    print(
        f"\n[bold red]File '{filename}' does not exist. Please correct the file path and try again[/]"
    )
    exit()

