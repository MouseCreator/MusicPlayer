from abc import ABC, abstractmethod

from data import RepeatOption, UserCache


class CacheService(ABC):
    @abstractmethod
    def update_last_path(self, last_path: str):
        pass

    @abstractmethod
    def update_repeat_option(self, repeat: RepeatOption):
        pass

    @abstractmethod
    def update_last_volume(self, volume: int):
        pass

    @abstractmethod
    def load_cache(self) -> UserCache:
        pass


class CacheServiceImpl(ABC):
    @abstractmethod
    def update_last_path(self, last_path: str):
        cached_data = self.load_cache()
        cached_data.last_directory = last_path
        self._save_cache(cached_data)
    @abstractmethod
    def update_repeat_option(self, repeat: RepeatOption):
        cached_data = self.load_cache()
        cached_data.repeat = repeat
        self._save_cache(cached_data)

    @abstractmethod
    def update_last_volume(self, volume: int):
        cached_data = self.load_cache()
        cached_data.last_volume = volume
        self._save_cache(cached_data)

    @abstractmethod
    def load_cache(self) -> UserCache:
        pass

    def _save_cache(self, cached_data: UserCache):
        pass