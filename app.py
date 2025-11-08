import tkinter as tk

from database import DataBase
from elements import CoreLayout
from events import EventRegistry
from player.PygletPlayer import PygletPlayer

class Application:

    def __init__(self):
        self.root = tk.Tk()
        self.event_registry = EventRegistry()
        self.database = DataBase(self.event_registry)
        self.player = PygletPlayer()

    def _setup_layout(self):
        self.core = CoreLayout(self.root, self.event_registry, self.database)

    def begin(self):
        self._setup_layout()
        self.player.set_file('melodies/melody.wav')
        self.player.play()
        self.root.mainloop()


if __name__ == '__main__':
    player = Application()
    player.begin()