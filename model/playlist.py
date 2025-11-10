
from typing import List, Self
from data import Music
from model.callback import Callback

class Playlist:

    def __init__(self, callback: Callback[Self]):
        self.callback = callback
        self.music_list = []

    def append(self, music_list: List[Music]):
        self.music_list.extend(music_list)
        self.callback.call(self)

    def view(self) -> List[Music]:
        return list(self.music_list)

    def set_position(self, music: Music, position: int):
        self.music_list.remove(music)
        self.music_list.insert(position, music)
        self.callback.call(self)

    def remove(self, music: Music):
        self.music_list.remove(music)
        self.callback.call(self)

    def clear(self):
        self.music_list.clear()
        self.callback.call(self)

