from player.abstract_player import AbstractPlayer
import pyglet
from typing import Optional

class PygletPlayer(AbstractPlayer):

    def __init__(self) -> None:
        self._player: pyglet.media.Player = pyglet.media.Player()
        self._source: Optional[pyglet.media.Source] = None
        self._paused: bool = False
        self._ended: bool = False

        @self._player.event
        def on_eos():
            self._ended = True
            self._player.pause()
        self._player.eos_action = 'pause'

    def _has_media(self) -> bool:
        return self._source is not None

    def set_file(self, filepath: str):
        try:
            self._player.delete()
        except Exception:
            raise RuntimeError('Unable to delete player')

        self._player = pyglet.media.Player()
        self._player.eos_action = 'pause'
        self._paused = False
        self._ended = False

        @self._player.event
        def on_eos():
            self._ended = True
            self._player.pause()
        self._source = pyglet.media.load(filepath, streaming=True)
        self._player.queue(self._source)

    def play(self):
        if not self._has_media():
            raise RuntimeError("No media loaded.")
        if self._ended:
            return
        self._player.play()
        self._paused = False

    def pause(self):
        if not self._has_media():
            return
        self._player.pause()
        self._paused = True

    def resume(self):
        if not self._has_media():
            return
        if self._ended:
            return
        self._player.play()
        self._paused = False

    def get_state(self) -> str:
        if not self._has_media():
            return "finished"
        if self._player.playing:
            return "playing"
        if self._ended:
            return "finished"
        if self._paused:
            return "paused"
        return "finished"

    def get_time_millis(self) -> int:
        if not self._has_media():
            return 0
        return int(self._player.time * 1000)


    def set_volume(self, volume: int):
        if not self._has_media():
            return
        v = volume / 100.0
        self._player.volume = float(v)

    def set_speed(self, speed: float):
        if not self._has_media():
            return
        pct = max(0.1, speed)
        self._player.pitch = float(pct)

    def set_time_millis(self, millis: int):
        if not self._has_media():
            return
        seconds = max(0.0, millis / 1000.0)
        try:
            self._player.seek(seconds)
            self._ended = False
        except Exception:
            raise RuntimeError('Unable to update time millis')