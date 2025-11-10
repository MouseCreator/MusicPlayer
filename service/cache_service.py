from model.cached_data import CachedData
from model.model_event import LoadStateEventListener, MusicStateEventListener, LoadStateEvent, MusicStateEvent


class CacheService(LoadStateEventListener, MusicStateEventListener):

    _cache: CachedData

    def _save(self):
        pass

    def get_cache(self) -> CachedData:
        return self._cache.clone()

    def on_music_state_event(self, event: MusicStateEvent):
        self._cache.last_repeat = event.get().get_record().repeat_option
        self._cache.last_volume = event.get().get_record().volume
        self._save()

    def on_load_sate_event(self, event: LoadStateEvent):
        self._cache.last_folder = event.get().get_last_folder()
        self._save()

