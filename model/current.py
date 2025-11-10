from typing import Self

from data import Music
from model.callback import Callback


class CurrentSong:
    _music: None | Music

    def __init__(self, callback: Callback[Self]):
        self._music = None
        self._callback = callback

    def set_current(self, music: Music):
        self._music = music
        self._callback.call(self)