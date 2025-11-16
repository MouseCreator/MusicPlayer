from typing import List
from uuid import uuid4

from model.callback import EmptyCallback
from model.music import Music
from model.playlist import Playlist

def _init_music(named: str) -> Music:
    music = Music()
    music.id = uuid4()
    music.name = named
    music.duration_millis = 1000
    music.extension = "mp3"
    music.filename = named + "mp3"
    return music

def _init_list() -> List[Music]:
    return [
        _init_music("a"),
        _init_music("d"),
        _init_music("c"),
        _init_music("b"),
    ]

def test_sort_playlist():
    playlist = Playlist(EmptyCallback())
    playlist.append(_init_list())

    assert len(playlist.view()) == 4

    playlist.sort()
    view = playlist.view()
    assert len(view) == 4

    for i, s in enumerate(view):
        assert s.name == chr(ord('a') + i)
