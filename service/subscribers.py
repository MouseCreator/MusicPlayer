from abc import abstractmethod, ABC
from typing import TypeVar, Type, List, Tuple

from model.model_event import ModelEvent, EventListener

T = TypeVar('T')

class Subscribers(ABC):
    @abstractmethod
    def publish(self, event: ModelEvent):
        pass
    @abstractmethod
    def subscribe(self, listener: EventListener):
        pass

    def subscribe_all(self, listeners: List[EventListener]):
        for listener in listeners:
            self.subscribe(listener)

class MappedSubscribers(Subscribers):

    def __init__(self, listener_map: List[Tuple[Type[EventListener], Type, str]]):
        self.listener_map = listener_map
        self._handlers = {}

    def subscribe(self, listener: EventListener):

        for listener_type, event_type, method_name in self.listener_map:
            if isinstance(listener, listener_type):
                callback = getattr(listener, method_name)
                if event_type in self._handlers:
                    self._handlers[event_type].append(callback)
                else:
                    self._handlers[event_type] = [callback]

    def publish(self, event: ModelEvent[T]):
        payload_type = event.generic()
        handlers = self._handlers.get(payload_type)
        if not handlers:
            return
        for handler in handlers:
            handler(event)