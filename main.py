import core.config as config
import core.logs as logger
from core import socket

logs = logger.Logger()

if __name__ == "__main__":
    logs.info(
        "Welcome to ncspot-discord, The compatability layer for ncspot to Discord RPC."
    )

    if config.basic.VERSION != "?":
        logs.info(f"Application Version: {config.basic.VERSION}")
    elif config.basic.VERSION == "?":
        logs.warn(
            "Unable to find most current version, ensure you have the most recent update."
        )

    sock = socket.ListenerSocket()
    sock.start_sock()  ## Let it rip
