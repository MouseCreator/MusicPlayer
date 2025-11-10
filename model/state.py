from typing import Self

from callback import Callback, EmptyCallback


class StateRecord:
    volume: int
    speed: float
    last_folder: str | None

    def __init__(self):
        pass

    def clone(self) -> Self:
        pass

def initial_data() -> StateRecord:
    record = StateRecord()
    record.volume = 100
    record.speed = 1.0
    record.last_folder = None
    return record


class State:

    def __init__(self, callback: Callback[Self] | None, initial: StateRecord | None):
        if not callback:
            callback = EmptyCallback()

        if initial is None:
            initial = initial_data()
        self.state = initial
        self.callback = callback

    def get_record(self) -> StateRecord:
        return self.state.clone()
    def set_volume(self):
        self.callback.call(self)
    def set_speed(self):
        self.callback.call(self)
    def set_playing(self):
        self.callback.call(self)
