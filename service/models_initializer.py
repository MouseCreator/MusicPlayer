from abc import ABC, abstractmethod
from typing import TypeVar

from cache_service import CacheService
from model.callback import Callback
from model.current import CurrentSong
from model.load_state import LoadState
from model.model_event import ModelEvent
from model.models import Models
from model.musicstate import MusicState, StateRecord
from model.playlist import Playlist
from model.timer import MusicTimer
from service.subscribers import Subscribers


class ModelsInitializer(ABC):
    @abstractmethod
    def init_models(self) -> Models:
        pass

T = TypeVar('T')

class EventCallback(Callback[T]):

    def __init__(self, subs: Subscribers):
        self._subs = subs
    def call(self, t: T) -> None:
        event = ModelEvent(t)
        self._subs.publish(event)


class _CallbackGenerator:
    def __init__(self, subs: Subscribers):
        self._subs = subs

    def generate_event(self) -> EventCallback[T]:
        return EventCallback(self._subs)


class ModelsInitializerImpl(ModelsInitializer):

    def __init__(self, cache_service: CacheService, subs: Subscribers):
        self._cache_service = cache_service
        self._subs = subs

    def init_models(self) -> Models:
        callbacks = _CallbackGenerator(self._subs)
        cache = self._cache_service.load_cache()

        initial_settings = StateRecord()
        initial_settings.speed = 1.0
        initial_settings.volume = cache.last_volume
        initial_settings.repeat_option = cache.last_repeat

        current = CurrentSong(callback=callbacks.generate_event())
        playlist = Playlist(callback=callbacks.generate_event())
        state = MusicState(callback=callbacks.generate_event(), initial=initial_settings)
        timer = MusicTimer(callback=callbacks.generate_event())
        load_state = LoadState(callback=callbacks.generate_event())

        return Models(current, playlist, state, timer, load_state)