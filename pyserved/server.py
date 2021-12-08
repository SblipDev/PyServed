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


# import base64
"""
Client that sends the file (uploads)
"""


import socket
import tqdm
import os
import argparse
import readline
import sys

SEPARATOR = "<Order66>"
BUFFER_SIZE = 1024 * 100000  # 4KB


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

try:
    print("[INFO] : Program Initialized at current directory.")
    filename = input('[FILEPATH] : ')
    send_file(filename, SERVER, PORT)
    print("[INFO] : Got file path successfully.")
    print(f"[INFO] : Sending {filename} to {SERVER}:{PORT}")
    print(f"[INFO] : Sent file. :)")
except KeyboardInterrupt:
    print("\n[QUIT] : Keyboard Interrupt.")
    exit()
