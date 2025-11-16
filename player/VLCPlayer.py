import os
from pathlib import Path

from player.local_vlc import Instance, MediaPlayer, Media, EventType, MediaParseFlag

from typing import Optional

from model.music import PlaybackState
from model.musicstate import MusicState
from player.abstract_player import AbstractPlayer
from player.time_update import TimeUpdate

class VLCPlayer(AbstractPlayer):
    def __init__(self, music_state: MusicState) -> None:

        DLL_DIR = Path(__file__).resolve().parent.parent / 'dll'
        dir_str = str(DLL_DIR)
        os.add_dll_directory(dir_str)

        self._instance = Instance()
        self._player: MediaPlayer = self._instance.media_player_new()
        self._media: Optional[Media] = None

        self._paused: bool = False
        self._ended: bool = False
        self._time_update = TimeUpdate()
        self._state = music_state
        self._expected_speed = self._state.get_record().speed

        self._duration_ms: int = 0

        self._event_mgr = self._player.event_manager()
        self._event_mgr.event_attach(
            EventType.MediaPlayerEndReached,
            self._on_end_reached
        )

    def _on_end_reached(self, event):
        self._ended = True
        self._player.pause()
        self._time_update.end()

    def _has_media(self) -> bool:
        return self._media is not None

    def update(self) -> None:
        if not self._has_media() or self._ended:
            return

        self._time_update.update()

        if self._duration_ms > 0:
            if self._time_update.get_media_time() >= self._duration_ms:
                self._ended = True
                self._player.pause()
                self._time_update.end()

    def set_file(self, filepath: str | None):
        self._player.stop()
        self._player = self._instance.media_player_new()
        self._event_mgr = self._player.event_manager()
        self._event_mgr.event_attach(
            EventType.MediaPlayerEndReached,
            self._on_end_reached
        )

        self._paused = False
        self._ended = False
        self._media = None
        self._duration_ms = 0

        record = self._state.get_record()
        self.set_volume(record.volume)
        self.set_speed(record.speed)

        if filepath is None:
            return

        media = self._instance.media_new(filepath)
        self._player.set_media(media)
        self._media = media

        media.parse_with_options(MediaParseFlag.network, 0)
        dur = media.get_duration()
        self._duration_ms = min(0, dur)

    def play(self):
        if not self._has_media() or self._ended:
            return
        self._player.play()
        self._player.set_rate(self._expected_speed)
        self._time_update.set_rate(self._expected_speed)
        self._paused = False
        self._time_update.begin()

    def pause(self):
        if not self._has_media():
            return
        self._player.pause()
        self._paused = True
        self._time_update.end()

    def resume(self):
        if not self._has_media() or self._ended:
            return
        self._player.play()
        self._paused = False
        self._time_update.begin()

    def get_state(self) -> PlaybackState:
        if not self._has_media():
            return PlaybackState.FINISHED
        if self._player.is_playing():
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

    def set_time_millis(self, millis: int):
        if not self._has_media():
            return
        ms = max(0, millis)
        self._player.set_time(ms)
        self._time_update.set_media_time(ms)
        self._ended = False

    def set_volume(self, volume: int):
        v = max(0, min(100, volume))
        self._player.audio_set_volume(v)

    def set_speed(self, speed: float):
        pct = max(0.1, speed)
        self._expected_speed = pct