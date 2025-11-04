from data import MusicState, RepeatOption, MusicSettings


class CacheService:
    def get_last_folder(self):
        pass
    def update_last_folder(self, folder: str):
        pass
    def update_last_volume(self):
        pass
    def update_last_repeat(self):
        pass

class MusicSettingsService:
    def __init__(self, settings: MusicSettings, cache_service: CacheService):
        self.settings = settings
        self.cache_service = cache_service

    def update_playback(self) -> MusicState:
        if self.settings.state == MusicState.FINISHED:
            self.settings.time = 0
            self.settings.state = MusicState.PLAYING
        elif self.settings.state == MusicState.PLAYING:
            self.settings.state = MusicState.PAUSED
        elif self.settings.state == MusicState.PAUSED:
            self.settings.state = MusicState.PLAYING
        return self.settings.state

    def finish(self):
        self.settings.state = MusicState.FINISHED

    def update_speed(self, speed: float) -> None:
        self.settings.speed = speed

    def update_volume(self, volume: int) -> None:
        self.settings.volume = volume

    def update_time(self, millis: int) -> None:
        self.settings.time = millis

    def update_repeat(self) -> RepeatOption:
        prev = self.settings.repeat
        if prev == RepeatOption.NO_REPEAT:
            self.settings.repeat = RepeatOption.REPEAT_ALL
        elif prev == RepeatOption.REPEAT_ALL:
            self.settings.repeat = RepeatOption.REPEAT_ONE
        elif prev == RepeatOption.REPEAT_ONE:
            self.settings.repeat = RepeatOption.NO_REPEAT
        return prev
