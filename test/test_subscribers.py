from typing import List

from model.cached_data import CachedData
from model.model_event import EventListener, ModelEvent, ListenerMapProvider, MusicStateEventListener
from model.models import Models
from model.music import RepeatOption
from model.musicstate import MusicState
from service.cache_service import CacheService
from service.models_initializer import ModelsInitializerImpl
from service.subscribers import MappedSubscribers

class MockSubscriber(EventListener):
    listened: List[str]
    def __init__(self):
        self.listened = []

    def on_event(self, event: ModelEvent[str]):
        self.listened.append(event.get())

def test_subscribers():
    listener_map = [
        (MockSubscriber, str, "on_event")
    ]
    mapped_subs = MappedSubscribers(listener_map)

    sub1 = MockSubscriber()
    sub2 = MockSubscriber()

    mapped_subs.subscribe_all([sub1, sub2])

    events = ["event1", "event2", "event3"]

    for event in events:
        mapped_subs.publish(event)

    assert sub1.listened == events
    assert sub2.listened == events


class MockedCache(CacheService):
    def get_cache(self) -> CachedData:
        data = CachedData()
        data.last_folder = ''
        data.last_repeat = RepeatOption.NO_REPEAT
        data.last_volume = 100
        return data

class RepeatOptionsListener(MusicStateEventListener):

    def __init__(self):
        self.repeat = RepeatOption.NO_REPEAT

    def on_music_state_event(self, event: ModelEvent[MusicState]):
        self.repeat = event.get().get_record().repeat_option


def test_integrated_subscribers():
    listener_map = ListenerMapProvider.provide()
    mapped_subs = MappedSubscribers(listener_map)

    repeat_listener = RepeatOptionsListener()
    mapped_subs.subscribe(repeat_listener)

    models: Models = ModelsInitializerImpl(MockedCache(), mapped_subs).init_models()
    music_state = models.state

    music_state.set_repeat_option(RepeatOption.NO_REPEAT)
    assert repeat_listener.repeat == RepeatOption.NO_REPEAT

    music_state.set_repeat_option(RepeatOption.NO_REPEAT)
    assert repeat_listener.repeat == RepeatOption.NO_REPEAT

    music_state.set_repeat_option(RepeatOption.REPEAT_ALL)
    assert repeat_listener.repeat == RepeatOption.REPEAT_ALL

    music_state.set_repeat_option(RepeatOption.REPEAT_ONE)
    assert repeat_listener.repeat == RepeatOption.REPEAT_ONE








