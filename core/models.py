from enum import Enum
from typing import List, Optional

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
    state: Optional[str] = None
    details: Optional[str] = None
    activity_type: Optional[ActivityType] = None
    large_img: Optional[str] = None
    large_img_text: Optional[str] = None
    large_img_link: Optional[str] = None
    small_img: Optional[str] = None
    small_img_text: Optional[str] = None
    small_img_link: Optional[str] = None
    state_url: Optional[str] = None
    details_url: Optional[str] = None
    ts_start: Optional[int] = None
    ts_end: Optional[int] = None
    party_id: Optional[str] = None
    party_size: Optional[list] = None
    join_secret: Optional[str] = None
    spectate_secret: Optional[str] = None
    match_secret: Optional[str] = None
    buttons: Optional[list] = None
    clear: bool = False


class SpotifyResponse(BaseModel):
    mode: Mode
    playable: Playable
