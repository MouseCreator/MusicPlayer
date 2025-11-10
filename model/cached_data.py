from typing import Self

from model.music import RepeatOption


class CachedData:
    last_folder: str
    last_volume: int
    last_repeat: RepeatOption
    def __init__(self):
        self.last_folder = ""
        self.last_volume = 50
        self.last_repeat = RepeatOption.NO_REPEAT

    def clone(self) -> Self:
        _copy = CachedData()
        _copy.last_repeat = self.last_repeat
        _copy.last_volume = self.last_volume
        _copy.last_folder = self.last_folder
        return _copy
