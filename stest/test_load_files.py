import unittest
from time import sleep

from model.cached_data import CachedData
from model.music import RepeatOption
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

    def test_load_files(self):
        system = _before_each()
        system.controllers.control.load_file(_music_files_provider)
        sleep(2)
        system.controllers.bottom.on_pause()