from abc import ABC, abstractmethod


class AbstractPlayer(ABC):
    @abstractmethod
    def set_file(self, filepath: str):
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
    def get_state(self) -> str:
        pass
    @abstractmethod
    def get_time_millis(self) -> int:
        pass

    @abstractmethod
    def set_time_millis(self, millis: int):
        pass
