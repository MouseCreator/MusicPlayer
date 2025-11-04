import tkinter as tk

from database import DataBase
from elements import CoreLayout
from events import EventRegistry

class MusicPlayer:

    def __init__(self):
        self.root = tk.Tk()
        self.event_registry = EventRegistry()
        self.database = DataBase(self.event_registry)

    def _setup_layout(self):
        self.core = CoreLayout(self.root, self.event_registry, self.database)

    def begin(self):
        self._setup_layout()
        self.root.mainloop()


if __name__ == '__main__':
    player = MusicPlayer()
    player.begin()