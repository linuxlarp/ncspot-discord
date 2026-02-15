from core import socket
import core.config as config
import core.logs as logger

logs = logger.Logger()

if __name__ == "__main__":
    logs.info("Starting ncspot-discord")

    sock = socket.ListenerSocket()

    sock.connect_sock()
