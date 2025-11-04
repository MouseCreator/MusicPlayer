from enum import Enum
from typing import List

class Music:
    id: int
    duration_millis: int
    filename: str
    extension: str
    name: str
    def __init__(self):
        self.id = -1
        self.duration_millis = 0
        self.filename = ""
        self.extension = ""
        self.name = ""

class Playlist:
    music_list: List[Music]
    def __init__(self):
        self.music_list = []

class RepeatOption(Enum):
    NO_REPEAT = 1
    REPEAT_ONE = 2
    REPEAT_ALL = 3

class MusicState(Enum):
    PLAYING = 1
    PAUSED = 2
    FINISHED = 3

class MusicSettings:
    speed: float
    volume: int
    repeat: RepeatOption
    state: MusicState
    current_id: int
    time: int
    def __init__(self):
        self.current_id = -1
        self.speed = 1
        self.volume = 50
        self.repeat = RepeatOption.NO_REPEAT
        self.state = MusicState.PLAYING
        self.time = 0

class UserCache:
    last_volume: int
    last_directory: str | None
    repeat: RepeatOption

    def __init__(self):
        self.last_volume = 50
        self.last_directory = None
        self.repeat_option = RepeatOption.NO_REPEAT

