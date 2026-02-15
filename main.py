from core import config as config
from core import socket

if __name__ == "__main__":
    print(config.basic.DEBUG)

    sock = socket.ListenerSocket()

    sock.connect_sock()
