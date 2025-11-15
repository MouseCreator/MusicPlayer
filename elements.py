import os

import tkinter as tk
from tkinter import filedialog, ttk
from typing import List, Callable

from model.current import CurrentSong
from model.model_event import PlaylistEventListener, ModelEvent, PlaybackEventListener, MusicStateEventListener, \
    TimerEventListener, CurrentMusicEventListener
from model.models import Models
from model.music import Music, RepeatOption, PlaybackState
from model.musicstate import MusicState
from model.playback import Playback
from model.playlist import Playlist
from model.timer import MusicTimerEvent
from service.load_service import LoadService
from service.services import Services
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
        if files:
            self._models.load_state.set_last_folder(os.path.dirname(files[-1]))
            self._load_service.load_files(files)
    def _sort_list(self):
        self._models.playlist.sort()
    def _shuffle_list(self):
        self._models.playlist.shuffle()
    def _clear_list(self):
        self._models.current.clear()
        self._models.playlist.clear()

class MusicItem:
    def __init__(self,
                 parent: tk.Frame,
                 music: Music,
                 on_play: Callable[[Music], None],
                 on_remove: Callable[[Music], None],
                 on_drag_start,
                 on_drag_motion,
                 on_drag_release
                 ):
        self._on_play = on_play
        self._on_remove = on_remove

        self._on_drag_start = on_drag_start
        self._on_drag_motion = on_drag_motion
        self._on_drag_release = on_drag_release

        self._music = music
        self.item_frame = tk.Frame(parent, bd=1, relief=tk.RAISED, padx=5, pady=5)
        self.item_frame.pack(fill=tk.X, pady=2)

        self._name_label = tk.Label(self.item_frame, text=music.name, anchor="w")
        self._name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        dur_text = display_time(music.duration_millis)
        self._dur_label = tk.Label(self.item_frame, text=dur_text, width=6, anchor="e")
        self._dur_label.pack(side=tk.LEFT, padx=5)

        tk.Button(self.item_frame, text="Play", width=6, command=self._play).pack(side=tk.LEFT, padx=2)
        tk.Button(self.item_frame, text="Remove", width=7, command=self._remove).pack(side=tk.LEFT, padx=2)

        self.item_frame.bind("<ButtonPress-1>", self._drag_start)
        self.item_frame.bind("<B1-Motion>", self._drag_motion)
        self.item_frame.bind("<ButtonRelease-1>", self._drag_release)

        self._dur_label.bind("<ButtonPress-1>", self._drag_start)
        self._dur_label.bind("<B1-Motion>", self._drag_motion)
        self._dur_label.bind("<ButtonRelease-1>", self._drag_release)

        self._name_label.bind("<ButtonPress-1>", self._drag_start)
        self._name_label.bind("<B1-Motion>", self._drag_motion)
        self._name_label.bind("<ButtonRelease-1>", self._drag_release)

    def _play(self):
        self._on_play(self._music)
    def _remove(self):
        self._on_remove(self._music)

    def highlight(self):
        self.item_frame['bg'] = 'lightblue'

    def remove_highlight(self):
        self.item_frame['bg'] = 'white'

    def destroy(self):
        self.item_frame.destroy()

    def music(self):
        return self._music

    def _drag_start(self, event):
        self._on_drag_start(self, event)

    def _drag_motion(self, event):
        self._on_drag_motion(self, event)

    def _drag_release(self, event):
        self._on_drag_release(self, event)


class MusicList(PlaylistEventListener, CurrentMusicEventListener):

    def __init__(self, root: tk.Tk, models: Models):
        self._list_frame = tk.Frame(root)
        self._list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self._items: List[MusicItem] = []
        self._models = models

        self._canvas = tk.Canvas(self._list_frame)
        self._scrollbar = ttk.Scrollbar(self._list_frame, orient="vertical", command=self._canvas.yview)
        self._scrollable_frame = tk.Frame(self._canvas)

        self._scrollable_frame.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        )

        self._canvas.create_window((0, 0), window=self._scrollable_frame, anchor="nw")
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _on_play_music(self, music: Music):
        self._models.current.set_current(music)

    def _on_remove_music(self, music: Music):
        current = self._models.current.get_current()
        if not current:
            return
        if current == music:
            self._models.current.set_current(None)
        self._models.playlist.remove(music)


    def on_current_music_event(self, event: ModelEvent[CurrentSong]):
        current_music = event.get().get_current()
        self._apply_highlights(current_music)

    def _apply_highlights(self, current_music: Music):
        if current_music is None:
            return
        for item in self._items:
            if item.music() == current_music:
                item.highlight()
            else:
                item.remove_highlight()

    def on_playlist_event(self, event: ModelEvent[Playlist]):
        self._canvas.update_idletasks()
        self._canvas.pack_forget()
        for item in self._items:
            item.destroy()
        self._items = []
        playlist = event.get().view()
        for song in playlist:
            item = MusicItem(
                self._scrollable_frame,
                song,
                self._on_play_music,
                self._on_remove_music,
                self._on_drag_start_item,
                self._on_drag_motion_item,
                self._on_drag_release_item
            )
            self._items.append(item)
        self._apply_highlights(self._models.current.get_current())
        self._list_frame.pack()
        self._canvas.pack(fill=tk.BOTH, expand=True)

    def _on_drag_start_item(self, item: MusicItem, event):
        self._drag_item = item
        self._drag_start_y = event.y_root
        self._drag_index_start = self._items.index(item)
        item.item_frame.configure(relief=tk.SUNKEN)


    def _on_drag_motion_item(self, item: MusicItem, event):
        if self._drag_item is None:
            return

        y = event.y_root
        delta = y - self._drag_start_y

        if abs(delta) < 5:
            return

        abs_y = self._canvas.winfo_pointery() - self._scrollable_frame.winfo_rooty()

        target_index = None
        for i, it in enumerate(self._items):
            y1 = it.item_frame.winfo_y()
            y2 = y1 + it.item_frame.winfo_height()
            if y1 <= abs_y <= y2:
                target_index = i
                break

        if target_index is None:
            return

        current_index = self._items.index(self._drag_item)
        if target_index != current_index:
            self._items.pop(current_index)
            self._items.insert(target_index, self._drag_item)

            for it in self._items:
                it.item_frame.pack_forget()
            for it in self._items:
                it.item_frame.pack(fill=tk.X, pady=2)

    def _on_drag_release_item(self, item: MusicItem, event):
        if self._drag_item is None:
            return

        new_index = self._items.index(self._drag_item)
        self._drag_item.item_frame.configure(relief=tk.RAISED)

        if new_index != self._drag_index_start:
            playlist = self._models.playlist
            playlist.swap_index(self._drag_index_start, new_index)

        self._drag_item = None
        self._drag_index_start = None


class SeekFrame(TimerEventListener, CurrentMusicEventListener):

    def __init__(self, root: tk.Tk, models: Models):
        self._models = models
        self._seekbar = self._create_scale(root, 1)
        self._seekbar.pack(pady=20, padx=20, fill=tk.X)
        self._is_moved_by_user = False

    def _start_move(self, e):
        self._is_moved_by_user = True

    def _stop_move(self, e):
        self._is_moved_by_user = False
        self._models.timer.generate_event(int(float(self._seekbar.get())), True)

    def _create_scale(self, root: tk.Tk, max_val: int) -> ttk.Scale:
        scale = ttk.Scale(root, from_=0, to=max_val, orient=tk.HORIZONTAL)
        scale.bind("<Button-1>", self._start_move)
        scale.bind("<B1-Motion>", self._start_move)
        scale.bind("<ButtonRelease-1>", self._stop_move)
        return scale

    def _update(self, new_value):
        if not self._is_moved_by_user:
            self._seekbar.set(new_value)

    def on_timer_event(self, event: ModelEvent[MusicTimerEvent]):
        time_millis = event.get().time_millis
        self._update(time_millis)

    def on_current_music_event(self, event: ModelEvent[CurrentSong]):
        if not event.get().get_current():
            duration = 1
            self._seekbar.set(0)
        else:
            duration = event.get().get_current().duration_millis
        self._seekbar.config(to=duration)



class BottomPanel(CurrentMusicEventListener, TimerEventListener, PlaybackEventListener, MusicStateEventListener):

    def __init__(self, root: tk.Tk, models: Models):
        self._models = models
        self._bottom_frame = tk.Frame(root)
        self._bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

        self._time_label = tk.Label(self._bottom_frame, text="00:00")
        self._time_label.pack(side=tk.LEFT, padx=10)

        self._play_button = tk.Button(self._bottom_frame, text="▶️", command=self._on_play_pause)
        self._play_button.pack(side=tk.LEFT, padx=5)

        self._repeat_button = tk.Button(
            self._bottom_frame,
            text=self._repeat_text(self._models.state.get_record().repeat_option),
            command=self._on_repeat
        )
        self._repeat_button.pack(side=tk.LEFT, padx=5)

        tk.Label(self._bottom_frame, text="Speed:").pack(side=tk.LEFT, padx=(20, 5))
        self._speed_var = tk.StringVar(value="1.0")
        validator = (root.register(self._validate_speed), "%P")
        self._speed_spin = tk.Spinbox(
            self._bottom_frame,
            from_=0.1,
            to=8.0,
            increment=0.1,
            width=5,
            textvariable=self._speed_var,
            validate="key",
            validatecommand=validator,
            command=self._on_speed_change
        )
        self._speed_spin.pack(side=tk.LEFT)
        self._speed_spin.bind("<Return>", self._on_enter)

        self._volume_var = tk.IntVar(value=models.state.get_record().volume)

        self.volume_slider = tk.Scale(
            self._bottom_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self._volume_var,
            command=self._on_volume_change
        )
        self.volume_slider.pack(side=tk.LEFT)

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
        else:
            self._models.state.set_repeat_option(repeat)

    def _on_speed_change(self):
        self._models.state.set_speed(float(self._speed_spin.get()))

    def _on_volume_change(self, value):
        self._models.state.set_volume(int(round(float(value))))

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
            value = float(self._speed_var.get())
        except ValueError:
            value = 1
        if value < 0.1:
            value = 0.1
        elif value > 8:
            value = 8
        self._speed_var.set(f"{value:.1f}")
        self._on_speed_change()

    def on_music_state_event(self, event: ModelEvent[MusicState]):
        record = event.get().get_record()
        self._repeat_button.config(
            text=self._repeat_text(record.repeat_option)
        )
        self._speed_var.set(str(record.speed))
        self._volume_var.set(record.volume)

    def on_playback_changed(self, event: ModelEvent[Playback]):
        playback = event.get().get_playback()
        if playback == PlaybackState.PLAYING:
            self._play_button.config(text="⏸️")
        else:
            self._play_button.config(text="▶️")

    def _repeat_text(self, repeat: RepeatOption) -> str:
        if repeat == RepeatOption.NO_REPEAT:
            return "No repeat"
        elif repeat == RepeatOption.REPEAT_ALL:
            return "Repeat all"
        elif repeat == RepeatOption.REPEAT_ONE:
            return "Repeat one"
        else:
            return "!ERR!"
    def on_timer_event(self, event: ModelEvent[MusicTimerEvent]):
        millis = event.get().time_millis
        self._time_label.config(text=display_time(millis))
        self._time_label.pack(side=tk.LEFT, padx=10)

    def on_current_music_event(self, event: ModelEvent[CurrentSong]):
        self._time_label.config(text=display_time(0))


class CoreLayout:
    def __init__(self, root: tk.Tk, models: Models, services: Services, subs: Subscribers):
        self._control = ControlFrame(root, models, services.load_service)
        self._music_list = MusicList(root, models)
        self._seek = SeekFrame(root, models)
        self._bottom_panel = BottomPanel(root, models)
        subs.subscribe_all([self._seek, self._music_list, self._bottom_panel])
