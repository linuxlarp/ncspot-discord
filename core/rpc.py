import json
import os
import socket
import struct

import core.config as config
import core.logs as logger
import core.models as models

# Constants
OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2


class RPC:
    def __init__(self) -> None:
        self.config = config.basic
        self.logs = logger.Logger()

        self.client_id = self.config.API_CLIENT_ID
        self.display_pause = self.config.RPC_DISPLAY_PAUSE
        self.ipc_path = os.path.abspath(self.config.DISCORD_IPC_PATH)

        self.rpc = self.start_connection()

    def start_connection(self):
        self.logs.info("Attempting to start connection to Discord RPC.")
        self.socket: socket.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        self.client = self.socket.connect(self.ipc_path)

        self.logs.info("Made socket connection...")
        self.logs.info("Attempting handshake..")
        self.logs.debug(f"CLIENT_ID: {self.client_id}")

        self.handshake()

        return

    def _send(self, payload, op=OP_FRAME):
        self.logs.debug(payload)

        payload = json.dumps(payload).encode("UTF-8")
        header = struct.pack("<II", op, len(payload))
        self.socket.sendall(header + payload)

    def _recv(self):
        header = self.socket.recv(8)
        op, length = struct.unpack("<II", header)
        data = self.socket.recv(length)
        return op, json.loads(data.decode("UTF-8"))

    def handshake(self):
        self._send({"v": 1, "client_id": self.client_id}, op=OP_HANDSHAKE)

        op, data = self._recv()

        try:
            if data["cmd"] == "DISPATCH" and data["evt"] == "READY":
                self.logs.success(
                    "Handshake Successful: Successfully connected to Discord RPC!"
                )

                self.logs.debug(f"Handshake: {data}")

                self.logs.success(f"""
User Information:
- Name: {data["data"]["user"]["username"]}
- ID: {data["data"]["user"]["id"]}
                """)  # If anyone has a better idea how to implement this. let me know :)

                return True
            else:
                self.logs.warn("Failed to connect to Discord RPC!")
                return
        except KeyError:
            if data["code"] == 4000:
                self.logs.error(
                    "Detected an invalid client ID, please double-check your config."
                )
                raise Exception

    class CurrentTrack:
        def __init__(self, client, data: models.Playable) -> None:
            pass

        def update_data(self, paused: bool):
            return

        def kill(self):
            return
