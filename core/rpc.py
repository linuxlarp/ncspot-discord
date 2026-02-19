import json
import os
from ast import BoolOp, Return

import core.config as config
import core.logs as logger
import core.models as models


class RPC:
    def __init__(self) -> None:
        self.config = config.basic
        self.client_id = self.config.API_CLIENT_ID
        self.display_pause = self.config.RPC_DISPLAY_PAUSE

        self.client = self.start_connection()

    def start_connection(self):
        return

    class CurrentTrack:
        def __init__(self, client, data: models.Playable) -> None:
            pass

        def update_data(self, paused: bool):
            return

        def kill(self):
            return
