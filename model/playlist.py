from typing import List, Self

from algorithm.collection_helper import MusicCollectionHelper
from model.music import Music
from model.callback import Callback, EmptyCallback


class Playlist:

    def __init__(self, callback: Callback[Self] | None, collection_helper: MusicCollectionHelper):
        if not callback:
            callback = EmptyCallback()

        self._callback = callback
        self._music_list = []
        self._collection_helper = collection_helper

    def append(self, music_list: List[Music]):
        self._music_list.extend(music_list)
        self._callback.call(self)

    def set_position(self, music: Music, position: int):
        self._music_list.remove(music)
        self._music_list.insert(position, music)
        self._callback.call(self)

    def remove(self, music: Music):
        self._music_list.remove(music)
        self._callback.call(self)

    def clear(self):
        self._music_list.clear()
        self._callback.call(self)

    def shuffle(self):
        self._music_list = self._collection_helper.shuffle(self._music_list)
        self._callback.call(self)

    def sort(self):
        self._music_list = self._collection_helper.sort(self._music_list)
        self._callback.call(self)

    def view(self) -> List[Music]:
        return list(self._music_list)

    def index_of(self, music: Music):
        return self._music_list.index(music)

    def size(self):
        return len(self._music_list)

    def at_index(self, index: int):
        return self._music_list[index]

    def swap_index(self, from_index, to_index):
        song = self._music_list.pop(from_index)
        self._music_list.insert(to_index, song)
        self._callback.call(self)

