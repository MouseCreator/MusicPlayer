from abc import abstractmethod, ABC
from typing import TypeVar, Dict, Type, List, Callable

from model.current import CurrentSong
from model.load_state import LoadState
from model.model_event import ModelEvent, EventListener, LoadStateEventListener, MusicStateEventListener, \
    PlaylistEventListener, TimerEventListener, CurrentMusicEventListener, PlaybackEventListener
from model.musicstate import MusicState
from model.playback import Playback
from model.playlist import Playlist
from model.timer import MusicTimer

T = TypeVar('T')

class Subscribers(ABC):
    @abstractmethod
    def publish(self, event: ModelEvent):
        pass
    @abstractmethod
    def subscribe(self, listener: EventListener):
        pass

    def subscribe_all(self, listeners: List[EventListener]):
        for listener in listeners:
            self.subscribe(listener)


class MappedSubscribers(Subscribers):

    def __init__(self):
        self._handlers: Dict[Type, List[Callable[[ModelEvent], None]]] = {
            CurrentSong: [],
            MusicTimer: [],
            Playlist: [],
            MusicState: [],
            LoadState: [],
        }

    def subscribe(self, listener: EventListener):
        listener_map = [
            (CurrentMusicEventListener, CurrentSong, "on_current_music_event"),
            (TimerEventListener,        MusicTimer,  "on_timer_event"),
            (PlaylistEventListener,     Playlist,    "on_playlist_event"),
            (MusicStateEventListener,   MusicState,  "on_music_state_event"),
            (LoadStateEventListener,    LoadState,   "on_load_sate_event"),
            (PlaybackEventListener,     Playback,    "on_playback_changed")
        ]

        for listener_type, event_type, method_name in listener_map:
            if isinstance(listener, listener_type):
                callback = getattr(listener, method_name)
                self._handlers[event_type].append(callback)

    def publish(self, event: ModelEvent[T]):
        payload_type = event.generic()
        handlers = self._handlers.get(payload_type)
        if not handlers:
            return
        for handler in handlers:
            handler(event)