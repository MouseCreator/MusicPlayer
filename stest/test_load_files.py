import unittest
from time import sleep

from model.cached_data import CachedData
from model.music import RepeatOption, PlaybackState
from setup import System, ManualSystemSetup, Params

DATA_DIR = '../test_data/'

def _refresh_cache(system: System):
    cache_data = CachedData()
    cache_data.last_repeat = RepeatOption.NO_REPEAT
    cache_data.last_folder = ''
    cache_data.last_volume = 0
    system.services.cache_service.save_cache(cache_data)

def _before_each() -> System:
    p = Params()
    p.cache_file = DATA_DIR + 'test_cache.txt'
    system = ManualSystemSetup(p).create()
    _refresh_cache(system)
    return system


def _music_files_provider(_):
    return [DATA_DIR + 'friendly.ogg', DATA_DIR + 'respite.mp3', DATA_DIR + 'valley.wav']

class LoadingSTest(unittest.TestCase):

    def test_change_options(self):
        system = _before_each()
        system.controllers.control.load_file(_music_files_provider)
        system.controllers.bottom.on_pause()
        assert system.models.playback.get_playback() == PlaybackState.PAUSED
        sleep(1)
        system.controllers.bottom.on_pause()
        assert system.models.playback.get_playback() == PlaybackState.PLAYING
        sleep(1)
        system.controllers.bottom.on_pause()
        assert system.models.playback.get_playback() == PlaybackState.PAUSED

        system.controllers.bottom.on_volume_change(40)
        assert system.models.state.get_record().volume == 40

        system.controllers.bottom.on_speed_change(2)
        assert system.models.state.get_record().speed == 2

        assert system.models.state.get_record().repeat_option == RepeatOption.NO_REPEAT
        system.controllers.bottom.on_repeat()
        assert system.models.state.get_record().repeat_option == RepeatOption.REPEAT_ALL
        system.controllers.bottom.on_repeat()
        assert system.models.state.get_record().repeat_option == RepeatOption.REPEAT_ONE
        system.controllers.bottom.on_repeat()
        assert system.models.state.get_record().repeat_option == RepeatOption.NO_REPEAT

    def test_load_files(self):
        system = _before_each()
        system.controllers.control.load_file(_music_files_provider)
        sleep(2)
        system.controllers.bottom.on_pause()
        assert system.models.playback.get_playback() == PlaybackState.PAUSED
        assert 1500 < system.services.player_service.get_time_millis() < 2500

    def test_play_selected_melodies(self):
        system = _before_each()
        system.controllers.control.load_file(_music_files_provider)

        assert system.models.current.get_current() == system.models.playlist.view()[0]
        system.controllers.music_list.on_play_music(system.models.playlist.view()[1])

        assert system.models.current.get_current() == system.models.playlist.view()[1]
        system.controllers.music_list.on_play_music(system.models.playlist.view()[2])

        assert system.models.current.get_current() == system.models.playlist.view()[2]
        system.controllers.bottom.on_pause()

    def test_next_file_starts_playing(self):
        system = _before_each()
        system.controllers.bottom.on_volume_change(0)
        system.controllers.control.load_file(_music_files_provider)
        sleep(1)
        system.controllers.seek.seek(70000) # skip to the end of the song
        sleep(4)
        system.controllers.bottom.on_pause()
        assert system.models.playback.get_playback() == PlaybackState.PAUSED
        assert system.models.current.get_current() == system.models.playlist.view()[1]


    def test_can_manually_change_order(self):
        system = _before_each()
        system.controllers.control.load_file(_music_files_provider)
        system.controllers.bottom.on_pause()

        before_list = system.models.playlist.view()

        system.controllers.music_list.swap_index(0, 1)

        after_list = system.models.playlist.view()

        assert before_list[0] == after_list[1]
        assert before_list[1] == after_list[0]


