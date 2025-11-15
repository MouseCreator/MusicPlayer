from enum import Enum

class Music:
    id: str
    duration_millis: int
    filename: str
    extension: str
    name: str
    def __init__(self, identity: str = ""):
        self.id = identity
        self.duration_millis = 0
        self.filename = ""
        self.extension = ""
        self.name = ""
    def __eq__(self, other):
        return self.id == other.id

class RepeatOption(Enum):
    NO_REPEAT = 1
    REPEAT_ONE = 2
    REPEAT_ALL = 3

class PlaybackState(Enum):
    PLAYING = 1
    PAUSED = 2
    FINISHED = 3

