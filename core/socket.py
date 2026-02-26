import json
import os
import socket
import time
from multiprocessing import Array

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
        sock_name = os.path.basename(self.sock_path)
        self.logs.info("Waiting for socket file to appear...")

        if not os.path.exists(self.sock_path):
            i = inotify.adapters.Inotify()
            i.add_watch(self.config.RUNTIME_PATH)
            for event in i.event_gen(yield_nones=False):
                (_, type_names, _, filename) = event
                if filename == sock_name and "IN_CREATE" in type_names:
                    break

        self.logs.info("Socket file found, attempting connection...")
        self.connect_sock()

    def connect_sock(self):
        try:
            self.RPC = discord.RPC()
        except Exception as e:
            self.logs.error("Failed to launch Discord RPC Client!", e)
            return

        while True:
            self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                self.logs.info(f"Connecting to socket at {self.sock_path}...")
                self.client.connect(self.sock_path)
                self.logs.success("Successfully connected to socket!")
                self._read_loop()
            except Exception as e:
                self.logs.error("Socket error:", e)
            finally:
                self.client.close()

            self.logs.warn("Socket disconnected, waiting for it to return...")
            self._wait_for_socket()

    def _read_loop(self):
        while True:
            data = self.client.recv(1024).decode("utf-8")
            if not data:
                self.logs.warn("Connection closed by server")
                break

            self.logs.debug(f"Recv: {data}")
            formatted = json.loads(data)

            if any(
                state in str(formatted).lower()
                for state in ("paused", "stopped", "finishedtrack")
            ):
                self.logs.debug("Media paused, stopped or track ended")
                self.RPC.update_track(track=None, clear=True)
            else:
                model = models.SpotifyResponse(**formatted)
                self.RPC.update_track(model, clear=False)
                self.logs.debug(
                    f"Playing: {model.playable.title} by {model.playable.artists}"
                )

    def _wait_for_socket(self):
        i = inotify.adapters.Inotify()
        i.add_watch(str(self.config.RUNTIME_PATH))
        for event in i.event_gen(yield_nones=False):
            (_, type_names, _, filename) = event
            if filename == "ncspot.sock" and "IN_CREATE" in type_names:
                break
