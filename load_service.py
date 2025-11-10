from abc import ABC, abstractmethod
from typing import List

from cache_service import CacheService
from model.music import Playlist, UserCache, Music

def convert(files: List[str]) -> List[Music]:
    result = []
    for file in files:
        music = Music()
        result.append(music)
    return result

class LoadService(ABC):
    @abstractmethod
    def load_music(self, new_files: List[str]):
        pass

    @abstractmethod
    def get_initial_directory(self) -> str | None:
        pass

class RegularLoadServiceImpl(LoadService):
    def __init__(self, playlist: Playlist):
        self._playlist = playlist

    def load_music(self, new_files: List[str]):
        music_list = convert(new_files)
        self._playlist.music_list.extend(music_list)

    def get_initial_directory(self) -> str | None:
        return None

class CachableLoadServiceImpl(LoadService):
    def __init__(self, playlist: Playlist, user_cache: UserCache, cache_service : CacheService):
        self._playlist = playlist
        self._user_cache = user_cache
        self._cache_service = cache_service

    def load_music(self, new_files: List[str]):
        music_list = convert(new_files)
        self._playlist.music_list.extend(music_list)
        # add last directory to cache

    def get_initial_directory(self) -> str | None:
        return self._user_cache.last_directory

class Loader:
    def __init__(self, load_service: LoadService):
        self._load_service = load_service

    def load(self, filenames: List[str]):
        music_list = self._load_service.load_music(filenames)
        self._apply_music_list(music_list)

    def _apply_music_list(self, music_list: List[Music]):
        pass