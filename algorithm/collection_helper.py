from abc import abstractmethod, ABC
import random
from typing import List

from algorithm.shuffle_algorithm import shuffle_list
from algorithm.sort_algorithm import sort_list
from model.music import Music


class MusicCollectionHelper(ABC):
    @abstractmethod
    def sort(self, music: List[Music]) -> List[Music]:
        pass
    @abstractmethod
    def shuffle(self, music: List[Music]) -> List[Music]:
        pass

class CustomMusicCollectionHelper(MusicCollectionHelper):

    def sort(self, music: List[Music]) -> List[Music]:
        return sort_list(music)

    def shuffle(self, music: List[Music]) -> List[Music]:
        return shuffle_list(music)


class LibMusicCollectionHelper(MusicCollectionHelper):
    def sort(self, music: List[Music]) -> List[Music]:
        return sorted(music, key=lambda m: m.name)

    def shuffle(self, music: List[Music]) -> List[Music]:
        shuffled = music[:]
        random.shuffle(shuffled)
        return shuffled