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

class CurrentMusicEvent(ModelEvent[CurrentSong]):
    pass

class CurrentMusicEventListener(ABC):
    @abstractmethod
    def on_current_music_event(self, event: CurrentMusicEvent):
        pass

class TimerEvent(ModelEvent[MusicTimer]):
    pass

class TimerEventListener(ABC):
    @abstractmethod
    def on_timer_event(self, event: TimerEvent):
        pass

class PlaylistEvent(ModelEvent[Playlist]):
    pass

class PlaylistEventListener(ABC):
    @abstractmethod
    def on_playlist_event(self, event: PlaylistEvent):
        pass

class MusicStateEvent(ModelEvent[MusicState]):
    pass

class MusicStateEventListener(ABC):
    @abstractmethod
    def on_music_state_event(self, event: MusicStateEvent):
        pass

class LoadStateEvent(ModelEvent[LoadState]):
    pass

class LoadStateEventListener(ABC):
    @abstractmethod
    def on_load_sate_event(self, event: LoadStateEvent):
        pass

