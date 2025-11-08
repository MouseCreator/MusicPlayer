import time

import pygame
from player.abstract_player import AbstractPlayer


def global_time_millis():
    return time.time() * 1000

class PyGamePlayer(AbstractPlayer):
    def __init__(self):
        pygame.mixer.init()
        self.filepath = None
        self._paused = False
        self._start_time = 0
        self._pause_time = 0
        self._offset = 0
        self._length = 0

    def set_file(self, filepath: str):
        self.filepath = filepath
        pygame.mixer.music.load(filepath)
        self._length = pygame.mixer.Sound(filepath).get_length() * 1000
        self._start_time = 0
        self._pause_time = 0
        self._offset = 0
        self._paused = False

    def play(self):
        if not self.filepath:
            raise ValueError("No file set.")
        pygame.mixer.music.play(start=self._offset / 1000.0)
        self._start_time = global_time_millis() - self._offset
        self._paused = False

    def pause(self):
        if not self._paused:
            pygame.mixer.music.pause()
            self._pause_time = global_time_millis()
            self._paused = True

    def resume(self):
        if self._paused:
            pygame.mixer.music.unpause()
            self._offset += self._pause_time - self._start_time
            self._start_time = global_time_millis() - self._offset
            self._paused = False

    def get_state(self) -> str:
        if self._paused:
            return "paused"
        elif pygame.mixer.music.get_busy():
            return "playing"
        else:
            return "stopped"

    def get_time_millis(self) -> int:
        if self._paused:
            return int(self._pause_time - self._start_time)
        if not pygame.mixer.music.get_busy():
            return int(self._length)
        return int(global_time_millis() - self._start_time)

    def set_time_millis(self, millis: int):
        if not self.filepath:
            raise ValueError("No file loaded.")
        millis = max(0, min(millis, self._length))
        self._offset = millis
        was_playing = pygame.mixer.music.get_busy()
        pygame.mixer.music.stop()
        if was_playing:
            pygame.mixer.music.play(start=millis / 1000.0)
            self._start_time = global_time_millis() - millis
            self._paused = False
        else:
            self._paused = True