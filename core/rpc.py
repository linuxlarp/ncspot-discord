import os
import time

import inotify
from pypresence import Presence
from pypresence.exceptions import DiscordNotFound, PipeClosed
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
        self.show_links = self.config.SHOW_LINKS
        self.client: Presence = Presence(self.client_id)

        while True:
            try:
                self.logs.info("Attempting to connect to Discord RPC...")
                self.client.connect()
                self.logs.success("Successfully connected to RPC!")
                break
            except Exception as e:
                if isinstance(e, DiscordNotFound):
                    self.logs.warn(
                        "Discord isnt running! Will wait until we're able to reconnect"
                    )

                    self.wait_for_ipc()
                else:
                    self.logs.error("Failed to connect to Discord RPC!", e)

    def update_track(self, track: Optional[models.SpotifyResponse], clear: bool):
        try:
            player_name = "ncspot"
            player_link = "https://github.com/hrkfdn/ncspot"

            if self.config.DISPLAY_CLIENT is False:
                player_name = "Spotify"
                player_link = "https://spotify.com"

            if clear:
                self.client.clear()
                return

            if track is not None:
                artists = ", ".join(str(artist) for artist in track.playable.artists)
                state = f"by {artists}"
                buttons = None

                if self.config.SHOW_LINKS:
                    buttons = [
                        {"label": "Play on Spotify", "url": track.playable.url},
                    ]

                self.client.update(
                    activity_type=ActivityType.LISTENING,
                    details=track.playable.title,
                    state=state,
                    name=player_name,
                    large_image=track.playable.cover_url,
                    large_text=f"on {track.playable.album}",
                    small_image=player_name.lower(),
                    small_text=player_name,
                    buttons=buttons,
                )
        except (DiscordNotFound, PipeClosed):
            self.logs.error("Lost RPC connection, reconnecting...")
            self.reconnect()

    def wait_for_ipc(self):
        i = inotify.adapters.Inotify()
        ipc_path = str(self.config.RUNTIME_PATH).strip("ncspot")
        ipc_name = "discord-ipc-0"

        i.add_watch(ipc_path)

        for event in i.event_gen(yield_nones=False):
            (_, type_names, _, filename) = event
            if filename == ipc_name and "IN_CREATE" in type_names:
                break

    def reconnect(self):
        while True:
            try:
                self.logs.info("Attempting to reconnect to Discord RPC...")
                self.client.connect()
                self.logs.success("Successfully reconnected!")
                break
            except (PipeClosed, DiscordNotFound):
                self.logs.error("Reconnect failed, waiting for IPC to appear.")
                self.wait_for_ipc()

    def disconnect(self):
        self.client.close()
        self.logs.success("Successfully closed RPC connection!")
