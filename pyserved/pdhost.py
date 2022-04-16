"""
deepthought@42 ~ $ pdhost

[SERVER]: started at 192.168.1.58:6789
192.168.1.58 - - [14/Apr/2022 20:05:28] "GET / HTTP/1.1" 200 -

The pdhost command included with PyServed Utilities is used
for hosting a folder on your network. The folder you host will be
accessible to anyone who has access to the network. You may change
the port by using the -port argument. The default port is 6789.
You will have to share the url shared at the fist line of the output.

This file is the code for the pdhost command.

Thanks for having interest in the project.
"""

# Import libraries

import http.server
import socketserver
from rich import print
import socket
import sys

# Function to get internal ip address


def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


# CHANGE DEFAULT PORT HERE
PORT = 6789
# CHANGE DEFAULT PORT HERE

# CHANGE HOST HERE
HOST = get_internal_ip()
# CHANGE HOST HERE

# Checks for the -port argument passed to the script
try:
    if sys.argv[1] is None:
        pass
    else:
        if "-port" in sys.argv[1]:
            PORT = int(sys.argv[2])
except IndexError:
    pass

# Sets handler to SimpleHTTPRequestHandler
handler = http.server.SimpleHTTPRequestHandler

# Starts server
try:
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[bold green][SERVER]:[/] started at {HOST}:" + str(PORT))
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n[bold red]KeyboardInterrupt[/]")
    exit()
except OSError:
    print(
        "\n[bold red]OSError: [Error 98] Address already in use.If not, please try again in a few seconds. If error message persists, please use the -port argument to set a new port.[/]"
    )

