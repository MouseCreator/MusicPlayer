from model.cached_data import CachedData
from model.model_event import MusicStateEventListener, ModelEvent, ListenerMapProvider
from model.models import Models
from model.music import RepeatOption
from model.musicstate import MusicState
from service.cache_service import CacheService
from service.models_initializer import ModelsInitializerImpl
from service.subscribers import MappedSubscribers


class MockedCache(CacheService):
    def save_cache(self, data: CachedData):
        pass

    def load_cache(self) -> CachedData:
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