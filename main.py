import core.config as config
import core.logs as logger
from core import socket

logs = logger.Logger()

if __name__ == "__main__":
    logs.info("Starting ncspot-discord")

    sock = socket.ListenerSocket()

    sock.start_sock()
