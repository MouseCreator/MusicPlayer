import tkinter as tk
from typing import List

from data import Music
from database import DataBase
from elements import CoreLayout
from events import EventRegistry
from player.PygletPlayer import PygletPlayer

class Application:
    core: CoreLayout | None
    def __init__(self):
        self.root = tk.Tk()
        self.event_registry = EventRegistry()
        self.database = DataBase(self.event_registry)
        self.player = PygletPlayer()
        self.core = None

    def _setup_layout(self):
        self.core = CoreLayout(self.root, self.event_registry, self.database)

    def begin(self):
        self._setup_layout()
        self.player.set_file('melodies/melody.wav')
        self.root.mainloop()

    def load(self, music_list: List[Music]):
        if not music_list:
            return
        self.core.add_music(music_list)
        self.select(music_list[0])

    def select(self, music: Music):
        pass


if __name__ == '__main__':
    player = Application()
    player.begin()