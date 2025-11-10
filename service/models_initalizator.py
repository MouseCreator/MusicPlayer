from abc import ABC, abstractmethod

from model.models import Models


class ModelsInitializator(ABC):
    @abstractmethod
    def init_models(self) -> Models:
        pass