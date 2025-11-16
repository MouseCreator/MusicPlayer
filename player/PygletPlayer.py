from model.music import PlaybackState
from model.musicstate import MusicState
from player.abstract_player import AbstractPlayer
import pyglet
from typing import Optional
from time_update import TimeUpdate


class PygletPlayer(AbstractPlayer):
    def __init__(self, state: MusicState) -> None:
        self._player: pyglet.media.Player = pyglet.media.Player()
        self._source: Optional[pyglet.media.Source] = None
        self._paused: bool = False
        self._ended: bool = False
        self._time_update = TimeUpdate()
        self._state = state

    def update(self) -> None:
        if not self._has_media():
            return
        if self._ended:
            return
        self._time_update.update()
        if self._time_update.get_media_time() >= (1000 * self._source.duration):
            self._ended = True
            self._player.pause()
            self._time_update.end()

    def _has_media(self) -> bool:
        return self._source is not None

    def set_file(self, filepath: str | None):
        try:
            self._player.delete()
        except Exception:
            raise RuntimeError('Unable to delete player')

        self._player = pyglet.media.Player()
        self._player.eos_action = 'pause'
        self._paused = False
        self._ended = False

        record = self._state.get_record()
        self.set_volume(record.volume)
        self.set_speed(record.speed)

        @self._player.event
        def on_eos():
            self._ended = True
            self._player.pause()

        if filepath is None:
            return
        self._source = pyglet.media.load(filepath, streaming=True)
        self._player.queue(self._source)

    def play(self):
        if not self._has_media():
            return
        if self._ended:
            return
        self._player.play()
        self._paused = False
        self._time_update.begin()

    def pause(self):
        if not self._has_media():
            return
        self._player.pause()
        self._time_update.end()
        self._paused = True

    def resume(self):
        if not self._has_media():
            return
        if self._ended:
            return
        self._player.play()
        self._time_update.begin()
        self._paused = False

    def get_state(self) -> PlaybackState:
        if not self._has_media():
            return PlaybackState.FINISHED
        if self._player.playing:
            return PlaybackState.PLAYING
        if self._ended:
            return PlaybackState.FINISHED
        if self._paused:
            return PlaybackState.PAUSED
        return PlaybackState.FINISHED

    def get_time_millis(self) -> int:
        if not self._has_media():
            return 0
        return self._time_update.get_media_time()


    def set_volume(self, volume: int):
        if not self._has_media():
            return
        v = volume / 100.0
        self._player.volume = float(v)

    def set_speed(self, speed: float):
        if not self._has_media():
            return
        pct = max(0.1, speed)
        self._player.pause()
        self._player.pitch = float(pct)
        self._player.play()
        self._time_update.set_rate(pct)

    def set_time_millis(self, millis: int):
        if not self._has_media():
            return
        seconds = max(0.0, millis / 1000.0)

        self._player.seek(seconds)
        self._time_update.set_media_time(millis)
        self._ended = False