from abc import abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Callback(Generic[T]):
    @abstractmethod
    def call(self, t: T) -> None:
        pass

class EmptyCallback(Callback):

    def call(self, t: T) -> None:
        pass
