"""
deepthought@42 ~ $ pdlisten

[{constants.success}] : Program Initialized at directory './'
[{constants.success}] : Enter Connection Key : 192@168@1@58+8080
[{constants.success}] : Set server ip to 192.168.1.58:8080
[{constants.success}] : Filename: file.txt

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
import constants

from rich import print
from rich.prompt import Prompt

# Variables

SEPARATOR = "<py42/>"
BUFFER_SIZE = 1024 * 100000

# Function for validating connection key and

def validate_key(key):
    # Correct key = 192@168@3@92+8080
    
    key_ca = key.split('@')
    if len(key_ca) == 4 and "+" in key_ca[3]:
        return True
    else:
        return False

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
        f"[bold green][{constants.success}][/] : Program Initialized at directory '{SAVE_DIR}'"
    )

    # Connection key prompt
    connectionkey = Prompt.ask(
        f"[bold green][{constants.success}][/] : Enter Connection Key "
    )
    
    if validate_key(connectionkey) is True: 
        print(
            f"[bold green][{constants.success}][/] : Set server ip to {keybreaker(connectionkey)}"
        )
    else:
        print(
            f"[bold red][{constants.error}][/] : Invalid Connection Key"
        )
        sys.exit(constants.exit)

    
    SERVER, PORT = tuple(keybreaker(connectionkey).split(":"))


    print(
        f"[bold green][{constants.success}][/] : Set server ip to {keybreaker(connectionkey)}"
    )

    # Prompts for file path
    filename = Prompt.ask(f"[bold green][{constants.success}][/] : Filename")

    # Send function.
    send_file(filename, SERVER, PORT)

    # Prints success message
    print(f"[bold green][{constants.success}][/] : Got file path successfully.")
    print(
        f"[bold green][{constants.success}][/] : Sending [bold yellow]{filename}[/] to {SERVER}:{PORT}"
    )
    print(f"[bold green][{constants.success}][/] : Sent file. :)")
except KeyboardInterrupt:
    # KeyboardInterrupt Error Handling
    print(f"\n\n[bold red][{constants.error}]: KeyboardInterrupt :( [/]")
    exit()
except ConnectionRefusedError:
    # ConnectionRefusedError Error Handling
    print(
        f"\n\n[bold red][{constants.error}]: Connection Refused. Please check the server program.[/]"
    )
    exit()
except FileNotFoundError:
    # FileNotFoundError Error Handling
    print(
        f"\n\n[bold red][{constants.error}]: File '{filename}' does not exist. Please correct the file path and try again[/]"
    )
    exit()
