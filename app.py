import tkinter as tk

from cache_service import CacheService
from model.models import Models
from model.music import Music
from elements import CoreLayout
from service.models_initializer import ModelsInitializerImpl, ModelsInitializer
from service.services import Services
from service.subscribers import Subscribers


class Application:
    core: CoreLayout | None
    services: Services | None
    models: Models | None
    subscribers: Subscribers | None

    def __init__(self):
        self.root = tk.Tk()

    def begin(self):
        self.subscribers = Subscribers()
        cache_service = CacheService()
        models_initializer = ModelsInitializerImpl(cache_service, self.subscribers)
        self.models = models_initializer.init_models()
        self.services = Services(self.subscribers, self.models)
        self.core = CoreLayout(self.root, self.models, self.services, self.subscribers)
        self.root.mainloop()

    def select(self, music: Music):
        pass


if __name__ == '__main__':
    player = Application()
    player.begin()