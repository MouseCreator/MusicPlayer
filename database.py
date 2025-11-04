from data import UserCache, MusicSettings, Playlist, MusicState, RepeatOption
from events import EventRegistry, PlaybackChangedEvent, SoundUpdatedEvent, SpeedUpdatedEvent, RepeatOptionChangedEvent, \
    StartSongEvent


class DataBase:
    def __init__(self, event_registry: EventRegistry):
        self._cache = UserCache()
        self._settings = MusicSettings()
        self._playlist = Playlist()
        self._event_registry = event_registry

    def get_cache(self) -> UserCache:
        return self._cache
    def get_settings(self) -> MusicSettings:
        return self._settings
    def get_playlist(self) -> Playlist:
        return self._playlist

    def update_playback(self, playback: MusicState | None = None):
        if playback is not None:
            self._settings.state = playback
        else:
            prev = self._settings.state
            if prev == MusicState.PLAYING:
                self._settings.state = MusicState.PAUSED
            if prev == MusicState.PAUSED:
                self._settings.state = MusicState.PLAYING
        self._event_registry.register("playback", PlaybackChangedEvent(self._settings.state))

    def update_sound(self, sound: int):
        self._settings.volume = sound
        self._event_registry.register("volume", SoundUpdatedEvent(sound))

    def update_speed(self, speed: float):
        self._settings.speed = speed
        self._event_registry.register("speed", SpeedUpdatedEvent(speed))

    def update_repeat(self, repeat_option: RepeatOption | None = None):
        if repeat_option is not None:
            self._settings.state = repeat_option
        else:
            prev = self._settings.repeat
            if prev == RepeatOption.NO_REPEAT:
                new = RepeatOption.REPEAT_ALL
            elif prev == RepeatOption.REPEAT_ALL:
                new = RepeatOption.REPEAT_ONE
            elif prev == RepeatOption.REPEAT_ONE:
                new = RepeatOption.NO_REPEAT
            else:
                new = prev
            self._settings.repeat = new
        self._event_registry.register("repeat", RepeatOptionChangedEvent(self._settings.repeat))

    def play_id(self, music_id: int):
        self._settings.current_id = music_id
        self._event_registry.register("song", StartSongEvent(music_id))