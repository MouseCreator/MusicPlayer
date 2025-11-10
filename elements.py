import os

import tkinter as tk
from tkinter import filedialog, ttk
from typing import List

from model.music import Music
from database import DataBase
from events import EventRegistry, LoadSongsEvent, SortSongsEvent, ShuffleSongsEvent, ClearSongsEvent
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

class MusicItem:
    def __init__(self, database: DataBase, parent: tk.Frame, music: Music):
        self.music = music
        self.database = database
        self.item_frame = tk.Frame(parent, bd=1, relief=tk.RAISED, padx=5, pady=5)
        self.item_frame.pack(fill=tk.X, pady=2)

        tk.Label(self.item_frame, text=music.name, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(self.item_frame, text=display_time(music.duration_millis), width=6, anchor="e").pack(side=tk.LEFT, padx=5)

        tk.Button(self.item_frame, text="Play", width=6, command=self.play).pack(side=tk.LEFT, padx=2)
        tk.Button(self.item_frame, text="Remove", width=7, command=self.remove).pack(side=tk.LEFT, padx=2)

    def play(self):
        self.database.play_id(self.music.id)
    def remove(self):
        self.item_frame.destroy()


class MusicList:
    def __init__(self, root: tk.Tk, event_registry: EventRegistry, database: DataBase):
        self.list_frame = tk.Frame(root)
        self.items: List[MusicItem] = []
        self.database = database
        self.event_registry = event_registry
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

    def _load_song(self, music: Music):
        item = MusicItem(self.database, self.list_frame, music)
        self.items.append(item)

    def _clear(self):
        for item in self.items:
            item.remove()
        self.items.clear()

    def add(self, musics: List[Music]):
        for s in musics:
            self._load_song(s)


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

class ControlFrame:
    def __init__(self, root: tk.Tk, event_registry: EventRegistry, database: DataBase):
        self._control_frame = tk.Frame(root)
        self._control_frame.pack(fill=tk.X, pady=5)
        self._event_registry = event_registry
        self._database = database

        tk.Button(self._control_frame, text="Load", command=self._load_file).pack(side=tk.LEFT, padx=5)
        tk.Button(self._control_frame, text="Sort", command=self._sort_list).pack(side=tk.LEFT, padx=5)
        tk.Button(self._control_frame, text="Shuffle", command=self._shuffle_list).pack(side=tk.LEFT, padx=5)
        tk.Button(self._control_frame, text="Clear", command=self._clear_list).pack(side=tk.LEFT, padx=5)

    def _load_file(self):
        paths = FileLoader.load(self._database.get_cache().last_directory)
        self._event_registry.register("list", LoadSongsEvent(paths))
    def _sort_list(self):
        self._event_registry.register("list", SortSongsEvent())
    def _shuffle_list(self):
        self._event_registry.register("list", ShuffleSongsEvent())
    def _clear_list(self):
        self._event_registry.register("list", ClearSongsEvent())

class BottomPanel:
    def __init__(self, root: tk.Tk, event_registry: EventRegistry, database: DataBase):
        self._event_registry = event_registry
        self._database = database
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
        self._database.update_playback()

    def _on_repeat(self):
        self._database.update_repeat()

    def _on_speed_change(self):
        self._database.update_speed(float(self.speed_spin.get()))

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

class CoreLayout:
    def __init__(self, root: tk.Tk, event_registry: EventRegistry, database: DataBase):
        self._control = ControlFrame(root, event_registry, database)
        self._seek = SeekFrame(root)
        self._music_list = MusicList(root, event_registry, database)
        self._bottom_panel = BottomPanel(root, event_registry, database)

    def add_music(self, musics: List[Music]):
        self._music_list.add(musics)
