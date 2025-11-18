from abc import ABC, abstractmethod

from model.model_event import ListenerMapProvider
from model.models import Models
from service.cache_service import FileCacheService
from service.models_initializer import ModelsInitializerImpl
from service.services import Services
from service.subscribers import Subscribers, MappedSubscribers
from ui.elements import ControllerLayer

class Params:
    def __init__(self):
        self.cache_file = "cache.txt"

class System:
    services: Services | None
    models: Models | None
    subscribers: Subscribers | None
    controllers: ControllerLayer | None
    def __init__(self,
                 services: Services,
                 models: Models,
                 subs: Subscribers,
                 controllers: ControllerLayer):
        self.models = models
        self.controllers = controllers
        self.subscribers = subs
        self.services = services

class SetupSystem(ABC):
    @abstractmethod
    def create(self) -> System:
        pass



class ManualSystemSetup(SetupSystem):
    def __init__(self, params: Params | None = None):
        if not params:
            params = Params()
        self.params = params

    def create(self) -> System:
        subscribers = MappedSubscribers(ListenerMapProvider.provide())
        cache_service = FileCacheService(cache_file=self.params.cache_file)
        models_initializer = ModelsInitializerImpl(cache_service, subscribers)
        models = models_initializer.init_models()
        services = Services(subscribers, models, cache_service)
        controllers = ControllerLayer(models, services)
        return System(services, models, subscribers, controllers)