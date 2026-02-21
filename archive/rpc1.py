import json
import os
import socket
import struct
from uuid import uuid4

import core.config as config
import core.logs as logger
import core.models as models
import core.utils as utils

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

        self.socket.connect(self.ipc_path)
        self.connected = True

        self.logs.info("Made socket connection...")
        self.logs.info("Attempting handshake..")
        self.logs.debug(f"CLIENT_ID: {self.client_id}")

        self.handshake()
        self.authenticate()

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

    def authenticate(self):
        self.logs.warn("I FUCKING HATE MY LIFE JUST FUCKING AUTHENTICATE")

        auth_payload = {
            "cmd": "AUTHORIZE",
            "args": {"client_id": self.client_id, "scopes": ["rpc", "identify"]},
            "nonce": utils.gen_nonce(),
        }

        self._send(auth_payload, op=OP_FRAME)
        resp = self._recv()

        self.logs.debug(f"Auth Response: {resp}")

    def handshake(self):
        self._send({"v": 1, "client_id": self.client_id}, op=OP_HANDSHAKE)

        op, data = self._recv()

        try:
            if data["cmd"] == "DISPATCH" and data["evt"] == "READY":
                self.logs.success(
                    "Handshake Successful: Successfully connected to Discord RPC!"
                )

                self.logs.debug(f"Handshake: {data}")

                return True
            else:
                self.logs.warn("Failed to connect to Discord RPC!")
                return
        except KeyError:
            if data["code"] == 4006:
                self.logs.error(
                    "Detected an invalid client ID, please double-check your config."
                )
                raise Exception

    def set_activity(self, Activity: models.Activity):
        if type(Activity.activity_type) != models.ActivityType:
            self.logs.error(
                "Unable to process activity change:", "ActivityType is invalid."
            )
            return

        if Activity.buttons and len(Activity.buttons) > 2:
            self.logs.error(
                "Unable top process activity change:",
                "You may not add more then 2 buttons to Activity.buttons",
            )

        act = utils.remove_none(
            {  ## Brace for impact
                "state": Activity.state,
                "details": Activity.details,
                "type": Activity.activity_type.value,
                "status_display_type": models.StatusDisplay.Name.value,
                "state_url": Activity.state_url,
                "details_url": Activity.details_url,
                "timestamps": {"start": Activity.ts_start, "end": Activity.ts_end},
                "assets": {
                    "large_image": Activity.large_img,
                    "large_text": Activity.large_img_text,
                    "large_url": Activity.large_img_link,
                    "small_image": Activity.small_img,
                    "small_text": Activity.small_img_text,
                    "small_url": Activity.small_img_link,
                },
                "party": {"id": Activity.party_id, "size": Activity.party_size},
                "secrets": {
                    "join": Activity.join_secret,
                    "spectate": Activity.spectate_secret,
                    "match": Activity.match_secret,
                },
                "buttons": Activity.buttons,
            }
        )

        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {"pid": os.getpid(), "activity": None if Activity.clear else act},
            "nonce": utils.gen_nonce(),
        }

        if not self.socket or not self.socket.connect:
            self.logs.warn(
                "Dropped connection when attempting to set activity, reconnecting.."
            )
            self.start_connection()

        try:
            self._send(payload, OP_FRAME)
            data = self._recv()

            self.logs.debug(f"RPC_RESPONSE: {data}")
        except Exception as e:
            self.logs.error("Failed to update RPC!", e)

        return

    def disconnect(self):
        self.logs.warn("Attempting to close RPC connection.")

        try:
            self._send({}, OP_CLOSE)
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()

            self.connected = False

            self.logs.success("Discord RPC connection closed!")
        except Exception as e:
            self.logs.debug("Socket closed before command was executed.", e)

    # Subclass for controling ncspot track data
    class CurrentTrack:
        def __init__(self, client, data: models.Playable) -> None:
            self.client: RPC = client

            act = models.Activity()

            act.activity_type = models.ActivityType.Listening
            act.state = "Test"
            act.details = "Hi testing for NCSPOT-DISCORD"

            self.client.set_activity(act)

            pass

        def update_data(self, paused: bool):
            return

        def kill(self):
            act = models.Activity()
            act.clear = True

            self.client.set_activity(act)
            return
