from sre_parse import State

from pypresence import Presence
from pypresence.types import ActivityType, StatusDisplayType

import core.config as config
import core.logs as logger
import core.models as models
import core.utils as utils


class RPC:
    def __init__(self) -> None:
        self.config = config.basic
        self.logs = logger.Logger()

        self.client_id = self.config.API_CLIENT_ID
        self.display_pause = self.config.RPC_DISPLAY_PAUSE
        self.client: Presence = Presence(self.client_id)

        try:
            self.logs.info("Attempting to connect to Discord RPC...")
            self.client.connect()
            self.logs.success("Successfully connected!")
        except Exception as e:
            self.logs.error("Failed to connect to Discord RPC!", e)

    def update_track(self, track: models.SpotifyResponse):
        self.client.update(state="Here it is!", details="NCSPOT!", name="Test 123456")

    def disconnect(self):
        self.client.close()
        self.logs.success("Successfully closed RPC connection!")
