import time


class TimeUpdate:
    def __init__(self):
        self._rate = 1.0
        self._last_ts = None
        self._media_time = 0.0
        self._playing = False

    def _global_time(self):
        return time.time()

    def set_media_time(self, millis: int):
        self._media_time = millis / 1000.0
        if self._playing:
            self._last_ts = self._global_time()

    def begin(self):
        self._playing = True
        self._last_ts = self._global_time()

    def set_rate(self, rate: float):
        self._rate = rate

    def end(self):
        self._playing = False
        self._last_ts = None

    def update(self):
        if self._playing:
            now = self._global_time()
            dt = now - self._last_ts
            self._media_time += dt * self._rate
            self._last_ts = now

    def get_media_time(self):
        return round(self._media_time * 1000)