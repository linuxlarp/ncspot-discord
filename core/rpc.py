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


class RPC:
    def __init__(self) -> None:
        self.config = config.basic
        self.logs = logger.Logger()

        self.client_id = self.config.API_CLIENT_ID
        self.client: Presence = Presence(self.client_id)

        while True:
            try:
                self.logs.info("Attempting to connect to Discord RPC...")
                self.client.connect()
                self.logs.success("Successfully connected to RPC!")
                self.logs.info("Play a song! We should be displaying content now.")
                break
            except Exception as e:
                if isinstance(e, DiscordNotFound):
                    self.logs.warn(
                        "Discord isnt running! Will wait until we're able to reconnect"
                    )

                    self._wait_for_ipc()
                else:
                    self.logs.error("Failed to connect to Discord RPC!", e)

    def update_track(self, track: Optional[models.SpotifyResponse], clear: bool):
        try:
            if clear:
                self.client.clear()
                return

            if track is not None:
                player_name = "ncspot"
                small_image = player_name.lower()
                start, end = None, None

                if self.config.DISPLAY_PLAYER_ICON is False:
                    small_image = None

                if self.config.DISPLAY_CLIENT is False:
                    player_name = "Spotify"

                artists = ", ".join(str(artist) for artist in track.playable.artists)
                state = f"by {artists}"

                if self.config.DISPLAY_PROGRESS is True:
                    start, end = self._calculate_ts(track)

                self.client.update(
                    activity_type=ActivityType.LISTENING,
                    details=track.playable.title,
                    state=state,
                    name=player_name,
                    large_image=track.playable.cover_url,
                    large_text=f"on {track.playable.album}",
                    small_image=small_image,
                    small_text=player_name,
                    start=start,
                    end=end,
                )

                if self.config.LOGS_ADD_SONG:
                    self.logs.info(
                        f"Now Playing: {track.playable.title} by {artists}, {track.playable.album}"
                    )

        except (DiscordNotFound, PipeClosed):
            self.logs.error("Lost RPC connection, reconnecting...")
            self._reconnect()

    def _wait_for_ipc(self):
        i = inotify.adapters.Inotify()
        ipc_path = str(self.config.RUNTIME_PATH).strip("ncspot")
        ipc_name = "discord-ipc-0"

        i.add_watch(ipc_path)

        for event in i.event_gen(yield_nones=False):
            (_, type_names, _, filename) = event
            if filename == ipc_name and "IN_CREATE" in type_names:
                break

    def _reconnect(self):
        while True:
            try:
                self.logs.info("Attempting to reconnect to Discord RPC...")
                self.client.connect()
                self.logs.success("Successfully reconnected!")
                break
            except (PipeClosed, DiscordNotFound):
                self.logs.error("Reconnect failed, waiting for IPC to appear.")
                self._wait_for_ipc()

    def disconnect(self):
        self.client.close()
        self.logs.success("Successfully closed RPC connection!")

    def _calculate_ts(self, track: models.SpotifyResponse) -> tuple[int, int]:
        secs = track.mode.Playing.secs_since_epoch
        nanos = track.mode.Playing.nanos_since_epoch
        duration = track.playable.duration / 1000  # ms > secs

        played_at = secs + (nanos / 1_000_000_000)

        now = time.time()
        elapsed = now - played_at

        start = int(played_at)
        end = int(played_at + duration)

        return start, end
