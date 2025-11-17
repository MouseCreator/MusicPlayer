import tkinter as tk

from model.models import Models
from setup import ManualSystemSetup
from ui.elements import CoreLayout
from service.services import Services
from service.subscribers import Subscribers


class Application:
    core: CoreLayout | None
    services: Services | None
    models: Models | None
    subscribers: Subscribers | None

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