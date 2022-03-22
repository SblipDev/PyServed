"""
Host file directory on network by using 'pdhost' command.
"""

import http.server
import socketserver
from rich import print
import socket
import sys

def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

PORT = 6789
HOST = get_internal_ip()

try:
    if sys.argv[1] is None:
        pass
    else:
        if '-port' in sys.argv[1]:
            PORT = int(sys.argv[2])
except IndexError:
    pass

handler = http.server.SimpleHTTPRequestHandler


try:
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[bold green][SERVER]:[/] started at {HOST}:" + str(PORT))
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n[bold red]KeyboardInterrupt[/]")
    exit()    
except OSError:
    print("\n[bold red]OSError: [Error 98] Address already in use.If not,please try again in a few seconds. If error message persists, please use the -port argument to set a new port.[/]")

