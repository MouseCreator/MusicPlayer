import os

from abstract_player import AbstractPlayer

os.add_dll_directory(os.getcwd())

import vlc

class VLCPlayer(AbstractPlayer):
    def get_state(self) -> str:
        return "null"

    _player: vlc.MediaPlayer

    def get_time_millis(self) -> int:
        return self._player.get_time()

    def set_time_millis(self, millis: int):
        self._player.set_time(millis)

    def __init__(self):
        self._filepath = None
        self._player = vlc.MediaPlayer()

    def set_file(self, filepath: str):
        self._filepath = filepath
        media = vlc.Media(self._filepath)
        self._player.set_media(media)

    def play(self):
        self._player.play()

    def pause(self):
        self._player.pause()

    def resume(self):
        self._player.pause()

    def stop(self):
        self._player.stop()