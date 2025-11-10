from typing import Self

from model.callback import Callback


class MusicTimer:
    _duration_millis: int
    _current_millis: int
    _is_playing: bool
    _callback: Callback[Self]

    def __init__(self, callback: Callback[Self]):
        self._callback = callback
        self._duration_millis = 0
        self._current_millis = 0
        self._is_playing = False

    def play(self):
        self._is_playing = True

    def stop(self):
        self._is_playing = False

    def update_time(self, millis_passed: int):
        if self._is_playing:
            self._current_millis = min(self._duration_millis, self._current_millis + millis_passed)
        self._callback.call(self)

    def set_time(self, millis: int):
        if millis < 0:
            millis = 0
        self._current_millis = min(millis, self._duration_millis)
        self._callback.call(self)