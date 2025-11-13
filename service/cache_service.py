
from model.cached_data import CachedData
from model.load_state import LoadState
from model.model_event import LoadStateEventListener, MusicStateEventListener, ModelEvent
from model.music import RepeatOption
from model.musicstate import MusicState
from service.property_file_service import PropertyFileService, PropertyFileServiceImpl


class CacheService(LoadStateEventListener, MusicStateEventListener):
    _cache: CachedData
    def __init__(self, property_file_service: PropertyFileService = PropertyFileServiceImpl(),
                 cache_file: str = "cache.txt"):
        self._cache_file = cache_file
        self._file_service = property_file_service
        self._load()

    def _load(self):
        props = self._file_service.load(self._cache_file)
        last_folder = props.get("last_folder")
        last_volume = int(props.get("last_volume", 50))
        repeat_raw = int(props.get("repeat_option", 1))
        try:
            last_repeat = RepeatOption(repeat_raw)
        except ValueError:
            last_repeat = RepeatOption.NO_REPEAT
        data = CachedData()
        data.last_folder = last_folder
        data.last_volume = last_volume
        data.last_repeat = last_repeat
        self._cache = data
        if not self._file_service.exists(self._cache_file):
            self._save()

    def _save(self):
        props = {
            "last_folder": self._cache.last_folder or "",
            "last_volume": str(self._cache.last_volume),
            "repeat_option": str(self._cache.last_repeat.value),
        }
        self._file_service.save(self._cache_file, props)

    def get_cache(self) -> CachedData:
        return self._cache.clone()

    def on_music_state_event(self, event: ModelEvent[MusicState]):
        self._cache.last_repeat = event.get().get_record().repeat_option
        self._cache.last_volume = event.get().get_record().volume
        self._save()

    def on_load_sate_event(self, event: ModelEvent[LoadState]):
        self._cache.last_folder = event.get().get_last_folder()
        self._save()

