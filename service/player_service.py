from model.current import CurrentSong
from model.model_event import MusicStateEventListener, ModelEvent, CurrentMusicEventListener, PlaybackEventListener, \
    TimerEventListener
from model.models import Models
from model.music import PlaybackState
from model.musicstate import MusicState
from model.playback import Playback
from model.timer import MusicTimerEvent
from player.abstract_player import AbstractPlayer
from service.repeat_service import RepeatService


class PlayerService(MusicStateEventListener, CurrentMusicEventListener, PlaybackEventListener, TimerEventListener):

    _player: AbstractPlayer

    def __init__(self, player: AbstractPlayer, models: Models, repeat_service: RepeatService):
        self._player = player
        self._models = models
        self._repeat_service = repeat_service
        self._just_finished = False

    def on_playback_changed(self, event: ModelEvent[Playback]):
        new_playback = event.get().get_playback()
        if new_playback == PlaybackState.FINISHED:
            self._repeat_service.on_song_finished()
        elif new_playback == PlaybackState.PLAYING:
            self._player.play()
        elif new_playback == PlaybackState.PAUSED:
            self._player.pause()

    def on_current_music_event(self, event: ModelEvent[CurrentSong]):
        music = event.get().get_current()
        if music is None:
            self._player.set_file(None)
        else:
            self._player.set_file(music.filename)
            self._models.playback.set_playback(PlaybackState.PLAYING)
        self._player.set_time_millis(0)

    def on_music_state_event(self, event: ModelEvent[MusicState]):
        music_record = event.get().get_record()
        self._player.set_speed(music_record.speed)
        self._player.set_volume(music_record.volume)

    def update_time_job(self):
        self._player.update()
        time_played = self._player.get_time_millis()
        player_state = self._player.get_state()
        if player_state == PlaybackState.PLAYING:
            self._models.timer.generate_event(time_played, False)
        if player_state == PlaybackState.FINISHED and not self._just_finished:
            self._just_finished = True
            self._models.playback.set_playback(PlaybackState.FINISHED)
        if self._just_finished and player_state != PlaybackState.FINISHED:
            self._just_finished = False

    def on_timer_event(self, event: ModelEvent[MusicTimerEvent]):
        if event.get().is_manual:
            self._player.set_time_millis(event.get().time_millis)