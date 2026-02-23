import os

from pypresence import Presence
from pypresence.types import ActivityType, StatusDisplayType
from typing_extensions import Optional

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

    def update_track(self, track: Optional[models.SpotifyResponse], clear: bool):
        player_name = "ncspot"

        if self.config.DISPLAY_CLIENT is False:
            player_name = "Spotify"

        if clear:
            self.client.clear()
            return

        if track is not None:
            artists = ", ".join(str(artist) for artist in track.playable.artists)
            state = f"by {artists}"

            if track.playable.album:
                state = f"by {artists} \n (on {track.playable.album}"

            self.client.update(
                activity_type=ActivityType.LISTENING,
                details=track.playable.title,
                state=state,
                name=player_name,
            )

    def disconnect(self):
        self.client.close()
        self.logs.success("Successfully closed RPC connection!")
