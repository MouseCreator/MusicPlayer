import tkinter as tk

from setup import ManualSystemSetup
from ui.elements import CoreLayout


class Application:
    core: CoreLayout | None
    root: tk.Tk

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Music Player")

    def begin(self):
        system = ManualSystemSetup().create()
        self.core = CoreLayout(self.root, system.controllers, system.subscribers)
        self.root.mainloop()


if __name__ == '__main__':
    player = Application()
    player.begin()