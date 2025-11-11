from typing import Self

from model.callback import Callback
from model.music import PlaybackState


class MusicTimer:
    _current_millis: int
    _playback_state: PlaybackState
    _callback: Callback[Self]

    def __init__(self, callback: Callback[Self]):
        self._callback = callback
        self._duration_millis = 0
        self._current_millis = 0
        self._playback_state = PlaybackState.FINISHED

    def set_playback_state(self, state: PlaybackState):
        self._playback_state = state
        self._callback.call(self)

    def get_playback_sate(self):
        return self._playback_state

    def update_time(self, millis: int):
        if millis < 0:
            millis = 0
        self._current_millis = millis
        self._callback.call(self)

    def get_time_millis(self) -> int:
        return self._current_millis