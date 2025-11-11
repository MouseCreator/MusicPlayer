import os

import tkinter as tk
from tkinter import filedialog, ttk
from typing import List

from model.model_event import PlaylistEventListener, ModelEvent, PlaybackEventListener, MusicStateEventListener
from model.models import Models
from model.music import Music, RepeatOption, PlaybackState
from model.musicstate import MusicState
from model.playback import Playback
from model.playlist import Playlist
from service.load_service import LoadService
from service.subscribers import Subscribers
from utils import display_time


class FileLoader:
    @staticmethod
    def load(initial_path: str | None) -> List[str] | None:
        filetypes = [
            ("Music files", ("*.mp3", "*.ogg", "*.wav")),
            ("All files", "*.*")
        ]
        filenames = filedialog.askopenfilenames(
            title="Select music files",
            initialdir=initial_path or os.getcwd(),
            filetypes=filetypes
        )
        if not filenames:
            return None
        abs_paths = [os.path.abspath(path) for path in filenames]
        return abs_paths


class ControlFrame:
    def __init__(self, root: tk.Tk, models: Models, load_service: LoadService):
        self._models = models
        self._load_service = load_service

        self._control_frame = tk.Frame(root)
        self._control_frame.pack(fill=tk.X, pady=5)

        tk.Button(self._control_frame, text="Load", command=self._load_file).pack(side=tk.LEFT, padx=5)
        tk.Button(self._control_frame, text="Sort", command=self._sort_list).pack(side=tk.LEFT, padx=5)
        tk.Button(self._control_frame, text="Shuffle", command=self._shuffle_list).pack(side=tk.LEFT, padx=5)
        tk.Button(self._control_frame, text="Clear", command=self._clear_list).pack(side=tk.LEFT, padx=5)

    def _load_file(self):
        last_folder = self._models.load_state.get_last_folder()
        files = FileLoader.load(last_folder)
        self._load_service.load_files(files)
    def _sort_list(self):
        self._models.playlist.sort()
    def _shuffle_list(self):
        self._models.playlist.shuffle()
    def _clear_list(self):
        self._models.playlist.clear()
        self._models.current.clear()

class MusicItem:
    def __init__(self, parent: tk.Frame, music: Music):
        self.music = music
        self.item_frame = tk.Frame(parent, bd=1, relief=tk.RAISED, padx=5, pady=5)
        self.item_frame.pack(fill=tk.X, pady=2)

        tk.Label(self.item_frame, text=music.name, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(self.item_frame, text=display_time(music.duration_millis), width=6, anchor="e").pack(side=tk.LEFT, padx=5)

        tk.Button(self.item_frame, text="Play", width=6, command=self.play).pack(side=tk.LEFT, padx=2)
        tk.Button(self.item_frame, text="Remove", width=7, command=self.remove).pack(side=tk.LEFT, padx=2)

    def play(self):
        pass
    def remove(self):
        pass


class MusicList(PlaylistEventListener):
    def on_playlist_event(self, event: ModelEvent[Playlist]):
        pass

    def __init__(self, root: tk.Tk):
        self.list_frame = tk.Frame(root)
        self.items: List[MusicItem] = []
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(self.list_frame)
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


class SeekFrame:
    def __init__(self, root: tk.Tk):
        self._seekbar = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self._on_scale_change)
        self._seekbar.pack(pady=20, padx=20, fill=tk.X)
        self._is_moved_by_user = False

    def _on_scale_change(self, value):
        pass

    def update(self, new_value):
        if self._is_moved_by_user:
            return
        self._seekbar.set(new_value)


class BottomPanel(PlaybackEventListener, MusicStateEventListener):

    def __init__(self, root: tk.Tk, models: Models):
        self._models = models
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

        self.time_label = tk.Label(self.bottom_frame, text="00:00")
        self.time_label.pack(side=tk.LEFT, padx=10)

        self.play_button = tk.Button(self.bottom_frame, text="Play", command=self._on_play_pause)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.repeat_button = tk.Button(self.bottom_frame, text="No repeat")
        self.repeat_button.pack(side=tk.LEFT, padx=5)

        tk.Label(self.bottom_frame, text="Speed:").pack(side=tk.LEFT, padx=(20, 5))
        self.speed_var = tk.StringVar(value="1.0")
        validator = (root.register(self._validate_speed), "%P")
        self.speed_spin = tk.Spinbox(
            self.bottom_frame,
            from_=0.1,
            to=8.0,
            increment=0.1,
            width=5,
            textvariable=self.speed_var,
            validate="key",
            validatecommand=validator,
            command=self._on_speed_change
        )
        self.speed_spin.pack(side=tk.LEFT)
        self.speed_spin.bind("<Return>", self._on_enter)

    def _on_play_pause(self):
        playback = self._models.playback.get_playback()
        if playback == PlaybackState.PLAYING:
            self._models.playback.set_playback(PlaybackState.PAUSED)
        elif playback == PlaybackState.PAUSED:
            self._models.playback.set_playback(PlaybackState.PLAYING)

    def _on_repeat(self):
        repeat = self._models.state.get_record().repeat_option
        if repeat == RepeatOption.NO_REPEAT:
            self._models.state.set_repeat_option(RepeatOption.REPEAT_ALL)
        elif repeat == RepeatOption.REPEAT_ALL:
            self._models.state.set_repeat_option(RepeatOption.REPEAT_ONE)
        elif repeat == RepeatOption.REPEAT_ONE:
            self._models.state.set_repeat_option(RepeatOption.NO_REPEAT)

    def _on_speed_change(self):
        self._models.state.set_speed(float(self.speed_spin.get()))

    def _on_volume_change(self):
        self._models.state.set_volume(100)

    def _validate_speed(self, new_value):
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def _on_enter(self, _):
        try:
            value = float(self.speed_var.get())
        except ValueError:
            value = 1
        if value < 0.1:
            value = 0.1
        elif value > 8:
            value = 8
        self.speed_var.set(f"{value:.1f}")
        self._on_speed_change()

    def on_music_state_event(self, event: ModelEvent[MusicState]):
        pass

    def on_playback_changed(self, event: ModelEvent[Playback]):
        pass

class CoreLayout:
    def __init__(self, root: tk.Tk, models: Models, subs: Subscribers):
        self._control = ControlFrame(root, models)
        self._seek = SeekFrame(root)
        self._music_list = MusicList(root)
        self._bottom_panel = BottomPanel(root)
        subs.subscribe_all([self._seek, self._music_list, self._bottom_panel])
