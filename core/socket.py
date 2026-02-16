import json
import os
import socket

import core.config as config
import core.logs as logger
import core.models as models


class ListenerSocket:
    def __init__(self) -> None:
        self.config = config.basic
        self.logs = logger.Logger()
        self.client: socket.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock_path = os.path.join(self.config.RUNTIME_PATH, "ncspot.sock")

    def start_sock(self):
        """Creates our asyncio loop for connect_sock"""

    def connect_sock(self):
        self.logs.info(
            f"Starting socket at {self.config.RUNTIME_PATH}/ncspot.sock ...."
        )
        self.logs.debug(self.config.RUNTIME_PATH)

        try:
            self.client.connect(self.sock_path)
            self.logs.success("Successfully connected to socket!")
        except Exception as e:
            self.logs.error(
                "Unexpected error occured in initial connection to socket:", e
            )

        try:
            while True:
                data = self.client.recv(1024).decode("utf-8")
                if data:
                    self.logs.debug(f"Recv: {data}")

                    formatted = json.loads(data)
                    model = models.SpotifyResponse(**formatted)

                    self.logs.debug(model.playable.title)
                else:
                    self.logs.warn("Client connection closed by server")
                    break

        except Exception as e:
            self.logs.error("Unexpected error occured in socket runtime:", e)
        finally:
            self.client.close()
            self.logs.warn("Socket connection terminated.")
