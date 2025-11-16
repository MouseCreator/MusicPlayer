import tkinter as tk

from model.model_event import ListenerMapProvider
from model.models import Models
from elements import CoreLayout
from service.cache_service import CacheService
from service.models_initializer import ModelsInitializerImpl
from service.services import Services
from service.subscribers import Subscribers, MappedSubscribers


class Application:
    core: CoreLayout | None
    services: Services | None
    models: Models | None
    subscribers: Subscribers | None

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Music Player")

    def begin(self):
        self.subscribers = MappedSubscribers(ListenerMapProvider.provide())
        cache_service = CacheService()
        models_initializer = ModelsInitializerImpl(cache_service, self.subscribers)
        self.models = models_initializer.init_models()
        self.services = Services(self.subscribers, self.models)
        self.core = CoreLayout(self.root, self.models, self.services, self.subscribers)
        self.root.mainloop()


if __name__ == '__main__':
    player = Application()
    player.begin()