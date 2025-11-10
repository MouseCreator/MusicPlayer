from typing import Self

from callback import Callback, EmptyCallback
from model.music import RepeatOption


class StateRecord:
    volume: int
    speed: float
    repeat_option: RepeatOption

    def __init__(self):
        pass

    def clone(self) -> Self:
        pass

def initial_data() -> StateRecord:
    record = StateRecord()
    record.volume = 100
    record.speed = 1.0
    record.repeat_option = RepeatOption.NO_REPEAT
    return record


class MusicState:

    def __init__(self, callback: Callback[Self] | None, initial: StateRecord | None):
        if not callback:
            callback = EmptyCallback()

        if initial is None:
            initial = initial_data()
        self._state = initial
        self._callback = callback

    def get_record(self) -> StateRecord:
        return self._state.clone()
    def set_volume(self):
        self._callback.call(self)
    def set_speed(self):
        self._callback.call(self)
    def set_playing(self):
        self._callback.call(self)
