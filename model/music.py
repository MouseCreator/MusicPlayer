from enum import Enum

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

class RepeatOption(Enum):
    NO_REPEAT = 1
    REPEAT_ONE = 2
    REPEAT_ALL = 3

class PlaybackState(Enum):
    PLAYING = 1
    PAUSED = 2
    FINISHED = 3

