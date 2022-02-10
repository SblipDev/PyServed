"""
________________________________
|                              |
| pyserved                     |
|                              |
| By:                          |
| Shaurya Pratap Singh         |
| 2021 ©                       |
|______________________________|
"""


# import base64
"""
Client that sends the file (uploads)
"""


import socket
import os
# import argparse
import readline
import sys

from rich import print
from rich.prompt import Prompt

SEPARATOR = "<[(^_^)]>"
BUFFER_SIZE = 1024 * 100000  


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


def get_internal_ip():
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss.connect(('8.8.8.8', 80))
    ip = ss.getsockname()[0]
    ss.close()
    return ip


SAVE_DIR = './'

SERVER = str(get_internal_ip())

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

DISCONNECT_MESSAGE = "!q"
FORMAT = 'utf-8'

keybreaker = lambda key: key.replace('@','.').replace('+', ':').strip(':')

try:
    print("[bold green][SERVER][/] : Program Initialized at current directory '{}'".format(SAVE_DIR))
    connectionkey = Prompt.ask("[bold green][SERVER][/] : Enter Connection Key ")
    print("[bold green][SERVER][/] : Set server ip to {}".format(keybreaker(connectionkey)))
    filename = Prompt.ask("[bold green][SERVER][/] : Filename")
    SERVER, PORT = tuple(keybreaker(connectionkey).split(':'))
    send_file(filename, SERVER, PORT)
    print("[bold green][SERVER][/] : Got file path successfully.")
    print(f"[bold green][SERVER[/] : Sending [bold yellow]{filename}[/] to {SERVER}:{PORT}")
    print(f"[bold green][SERVER][/] : Sent file. :)")
except KeyboardInterrupt:
    print("\n[bold red]KeyboardInterrupt[/]")
    exit()
except ConnectionRefusedError:
    print(f"\n[bold red]Connection Refused. Please check the server program.[/]")
    exit()
except FileNotFoundError:
    print(f"\n[bold red]File '{filename}' does not exist. Please correct the file path and try again[/]")
    exit()
