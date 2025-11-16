from model.models import Models
from player.VLCPlayer import VLCPlayer
from service.async_service import AsyncService
from service.cache_service import FileCacheService, FileCacheListener
from service.load_service import LoadService
from service.player_service import PlayerService
from service.repeat_service import RepeatService
from service.subscribers import Subscribers


class Services:
    load_service: LoadService
    repeat_service: RepeatService
    player_service: PlayerService
    cache_service: FileCacheService

    def __init__(self, subs: Subscribers, models: Models):
        self.load_service = LoadService(models)
        self.cache_service = FileCacheService()
        self.repeat_service = RepeatService(models)
        self.async_service = AsyncService()
        self.cache_listener = FileCacheListener(self.cache_service)
        self.player_service = PlayerService(VLCPlayer(models.state), models, self.repeat_service)
        self.async_service.schedule_every("update_time", 100, self.player_service.update_time_job)
        service_list = [self.cache_listener, self.player_service]
        subs.subscribe_all(service_list)