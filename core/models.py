from enum import Enum
from pydoc import classify_class_attrs
from typing import List

from pydantic import BaseModel, Field


# https://discord.com/developers/docs/events/gateway-events#activity-object-activity-types
class ActivityType(Enum):
    Playing = 0
    Streaming = 1
    Listening = 2
    Watching = 3
    Custom = 4
    Competing = 5


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


class Activity(BaseModel):
    state: str
    details: str
    activity_type: ActivityType

    large_img: str
    large_img_text: str
    large_img_link: str

    small_img: str
    small_img_text: str
    small_img_link: str

    state_url: str
    details_url: str

    ts_start: int
    ts_end: int

    party_id: str
    party_size: list
    join_secret: str
    spectate_secret: str
    match_secret: str
    buttons: list
    clear: bool


class SpotifyResponse(BaseModel):
    mode: Mode
    playable: Playable
