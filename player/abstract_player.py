from abc import ABC, abstractmethod

from model.music import PlaybackState


class AbstractPlayer(ABC):
    @abstractmethod
    def set_file(self, filepath: str | None):
        pass

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass

    @abstractmethod
    def get_state(self) -> PlaybackState:
        pass

    @abstractmethod
    def get_time_millis(self) -> int:
        pass

    @abstractmethod
    def set_volume(self, volume: int):
        pass

    @abstractmethod
    def set_speed(self, speed: float):
        pass

    @abstractmethod
    def set_time_millis(self, millis: int):
        pass
