from model.current import CurrentSong
from model.load_state import LoadState
from model.playback import Playback
from model.playlist import Playlist
from model.musicstate import MusicState
from model.timer import MusicTimer


class Models:
    current: CurrentSong
    playlist: Playlist
    state: MusicState
    timer: MusicTimer

    def __init__(self,
                 current: CurrentSong,
                 playlist: Playlist,
                 state: MusicState,
                 timer: MusicTimer,
                 load_state: LoadState,
                 playback: Playback
                 ):
        self.current = current
        self.playlist = playlist
        self.state = state
        self.timer = timer
        self.load_state = load_state
        self.playback = playback