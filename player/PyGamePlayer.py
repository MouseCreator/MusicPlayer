
import pygame

from model.music import PlaybackState
from player.abstract_player import AbstractPlayer

class PyGamePlayer(AbstractPlayer):
    def set_volume(self, volume: int):
        pass

    def set_speed(self, speed: float):
        pass

    def update(self) -> None:
        pass

    def __init__(self):
        pygame.mixer.init()
        self.filepath = None
        self._paused = False
        self._length = 0

    def set_file(self, filepath: str  | None):
        self.filepath = filepath
        pygame.mixer.music.load(filepath)
        self._length = pygame.mixer.Sound(filepath).get_length() * 1000
        self._paused = False

    def play(self):
        if not self.filepath:
            raise ValueError("No file set.")
        pygame.mixer.music.play()
        self._paused = False

    def pause(self):
        if not self._paused:
            pygame.mixer.music.pause()
            self._paused = True

    def resume(self):
        if self._paused:
            pygame.mixer.music.unpause()
            self._paused = False

    def get_state(self) -> PlaybackState:
        if self._paused:
            return PlaybackState.PAUSED
        elif pygame.mixer.music.get_busy():
            return PlaybackState.PLAYING
        else:
            return PlaybackState.FINISHED

    def get_time_millis(self) -> int:
        return pygame.mixer.music.get_pos()

    def set_time_millis(self, millis: int):
        if not self.filepath:
            raise ValueError("No file loaded.")
        millis = max(0, min(millis, self._length))
        was_playing = pygame.mixer.music.get_busy()
        pygame.mixer.music.stop()
        if was_playing:
            pygame.mixer.music.play(start=millis / 1000.0)
            self._paused = False
        else:
            self._paused = True