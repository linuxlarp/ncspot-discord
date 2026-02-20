from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class StatusDisplay(Enum):
    Name = 0
    State = 1
    Details = 2


class ModeDetails(BaseModel):
    secs_since_epoch: int
    nanos_since_epoch: int


class Mode(BaseModel):
    Playing: ModeDetails


class Playable(BaseModel):
    type: str
    id: str
    uri: str
    title: str
    track_number: int
    disc_number: int
    duration: int
    artists: List[str]
    artist_ids: List[str]
    album: str
    album_id: str
    album_artists: List[str]
    cover_url: str
    url: str
    added_at: str
    list_index: int
    is_local: bool
    is_playable: bool


class User(BaseModel):
    id: int
    username: str
    name: str
    avatar: str
    bot: bool


class SpotifyResponse(BaseModel):
    mode: Mode
    playable: Playable
