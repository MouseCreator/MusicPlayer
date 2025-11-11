from abc import abstractmethod, ABC
from typing import TypeVar, Generic

from model.current import CurrentSong
from model.load_state import LoadState
from model.musicstate import MusicState
from model.playlist import Playlist
from model.timer import MusicTimer

T = TypeVar('T')

class ModelEvent(ABC, Generic[T]):
    _t: T
    def __init__(self, t: T):
        self._t = t

    def get(self) -> T:
        return self._t


class CurrentMusicEventListener(ABC):
    @abstractmethod
    def on_current_music_event(self, event: ModelEvent[CurrentSong]):
        pass

class TimerEventListener(ABC):
    @abstractmethod
    def on_timer_event(self, event: ModelEvent[MusicTimer]):
        pass

class PlaylistEventListener(ABC):
    @abstractmethod
    def on_playlist_event(self, event: ModelEvent[Playlist]):
        pass

class MusicStateEventListener(ABC):
    @abstractmethod
    def on_music_state_event(self, event: ModelEvent[MusicState]):
        pass

class LoadStateEventListener(ABC):
    @abstractmethod
    def on_load_sate_event(self, event: ModelEvent[LoadState]):
        pass

