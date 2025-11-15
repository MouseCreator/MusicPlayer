from model.models import Models
from player.PygletPlayer import PygletPlayer
from service.async_service import AsyncService
from service.cache_service import CacheService
from service.load_service import LoadService
from service.player_service import PlayerService
from service.repeat_service import RepeatService
from service.subscribers import Subscribers


class Services:
    load_service: LoadService
    repeat_service: RepeatService
    player_service: PlayerService
    cache_service: CacheService

    def __init__(self, subs: Subscribers, models: Models):
        self.load_service = LoadService(models)
        self.cache_service = CacheService()
        self.repeat_service = RepeatService(models)
        self.async_service = AsyncService()
        self.player_service = PlayerService(PygletPlayer(models.state), models, self.repeat_service)
        self.async_service.schedule_every("update_time", 100, self.player_service.update_time_job)
        service_list = [self.cache_service, self.player_service]
        subs.subscribe_all(service_list)