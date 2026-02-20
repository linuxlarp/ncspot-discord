import json
import os
import socket
import time

import inotify.adapters

import core.config as config
import core.logs as logger
import core.models as models
import core.rpc as discord


class ListenerSocket:
    def __init__(self) -> None:
        self.config = config.basic
        self.logs = logger.Logger()
        self.client: socket.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock_path = os.path.join(self.config.RUNTIME_PATH, "ncspot.sock")

    def start_sock(self):
        """Creates our loop for connect_sock"""

        sock_name = os.path.basename(self.sock_path)

        self.logs.info("Waiting for socket file to appear...")

        while True:
            if os.path.exists(self.sock_path):
                self.logs.info("Socket file found, attempting connection")
                self.connect_sock()
                self.logs.warn("Socket disconnected, waiting for it to return")

            i = inotify.adapters.Inotify()
            i.add_watch(self.config.RUNTIME_PATH)

            for event in i.event_gen(yield_nones=False):
                (_, type_names, _, filename) = event
                if filename == sock_name and "IN_CREATE" in type_names:
                    break

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
                "Unexpected error occurred in initial connection to socket:", e
            )

        try:
            self.RPC = discord.RPC()
        except Exception as e:
            self.logs.error("Failed async launch", e)

        try:
            while True:
                data = self.client.recv(1024).decode("utf-8")
                if data:
                    self.logs.debug(f"Recv: {data}")

                    formatted = json.loads(data)

                    if any(
                        state in str(formatted).lower()
                        for state in ("paused", "stopped", "finishedtrack")
                    ):
                        self.logs.debug("Media paused, stopped or track ended")
                        ## Custom logic to update RPC or wait.. etc
                    else:
                        model = models.SpotifyResponse(**formatted)

                        ## Send parsed data to RPC

                        self.logs.debug(
                            f"Playing: {model.playable.title} by {model.playable.artists}"
                        )

                else:
                    self.logs.warn("Client connection closed by server")
                    break

        except Exception as e:
            self.logs.error("Unexpected error occured in socket runtime:", e)
        finally:
            self.client.close()
            self.logs.info("Socket connection terminated.")
