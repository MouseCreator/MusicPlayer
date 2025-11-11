from typing import Self

from model.callback import Callback
from model.music import PlaybackState


class Playback:
    def __init__(self, callback: Callback[Self]):
        self._callback = callback
        self._playback = PlaybackState.FINISHED
    def get_playback(self):
        return self._playback
    def set_playback(self, state: PlaybackState):
        self._playback = state