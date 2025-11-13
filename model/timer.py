
from model.callback import Callback

class MusicTimerEvent:
    def __init__(self,
                 time_millis: int,
                 is_manual: bool):
        self.time_millis = time_millis
        self.is_manual = is_manual

class MusicTimer:

    def __init__(self, callback: Callback[MusicTimerEvent]):
        self._callback = callback

    def generate_event(self, millis: int, manual: bool):
        self._callback.call(MusicTimerEvent(millis, manual))