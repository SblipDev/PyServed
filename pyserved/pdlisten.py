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

from rich import print

def keymaker(key: str) -> str:
    return key.replace('.', '@').replace(':','+')

HEADER = 64
class Client:
    def __init__(self, server, port):
        self.SERVER_HOST = server
        self.SERVER_PORT = port
        self.BUFFER_SIZE = 1024 * 100000
        self.SEPARATOR = "<[(^_^)]>"
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
        self.filesize = filesize
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

def is_port_in_use() -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((get_internal_ip(), PORT)) == 0

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

if is_port_in_use() is True:
    print("[bold red]Port 8080 is already in use in your network. Choose another port instead using the '-port' parameter.[/]")
    exit()

try:
    client = Client(SERVER, PORT)
    print("[bold green][SERVER]:[/] Server is listening on {}:{}".format(SERVER, PORT))
    print("[bold green][SERVER]:[/] Connection Key: {}".format(keymaker(str(SERVER+":"+str(PORT)))))
    print("[bold green][SERVER]:[/] Waiting for a connection for files...")
    client.listen()
    _, address = client.accept()
    print("[bold green][SERVER]:[/] Connection from {}:{} accepted.".format(address[0], address[1]))
    print("[bold green][SERVER]:[/] Reading file data.....")
    try:
        client.receive()
    except ValueError as e:
        print(f"{repr(e)} \n\n [bold red]An error occured. Please try again in few seconds....[/]")
        exit()
    print("[bold green][SERVER]:[/] Received file '[bold yellow]{}[/]', saving to current directory.".format(client.filename))
    client.write()
    print("[bold green][SERVER]:[/] File transferred successfully. Closing connection...")
    client.close()
except KeyboardInterrupt:
    print("\n[bold red]KeyboardInterrupt[/]")
    exit()
except Exception as e:
    print(f"\n[bold red] {repr(e)} \n\n If the problem presists, contact the owner of the package at https://github.com/SblipDev/pyserved[/] \n")
    exit()
    
