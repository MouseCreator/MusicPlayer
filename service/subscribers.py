from abc import abstractmethod, ABC
from inspect import signature
from typing import TypeVar, Type, List, Tuple

from model.model_event import ModelEvent, EventListener

T = TypeVar('T')

class Subscribers(ABC):
    @abstractmethod
    def publish(self, event: T):
        pass
    @abstractmethod
    def subscribe(self, listener: EventListener):
        pass

    def subscribe_all(self, listeners: List[EventListener]):
        for listener in listeners:
            self.subscribe(listener)

class MappedSubscribers(Subscribers):

    def __init__(self, listener_map: List[Tuple[Type[EventListener], Type, str]]):
        self._validate_map(listener_map)
        self.listener_map = listener_map
        self._handlers = {}

    def _validate_map(self, listener_map: List[Tuple[Type[EventListener], Type, str]]):
        for listener_class, event_type, method_name in listener_map:
            if not issubclass(listener_class, EventListener):
                raise TypeError(f"{listener_class.__name__} must be a subclass of EventListener")
            if not hasattr(listener_class, method_name):
                raise AttributeError(
                    f"{listener_class.__name__} is missing handler method '{method_name}'"
                )

            method = getattr(listener_class, method_name)

            sig = signature(method)
            params = list(sig.parameters.values())
            if len(params) != 2:
                raise TypeError(
                    f"Method '{method_name}' on {listener_class.__name__} must take exactly one argument"
                )

    def subscribe(self, listener: EventListener):
        added = False
        for listener_type, event_type, method_name in self.listener_map:
            if isinstance(listener, listener_type):
                added = True
                callback = getattr(listener, method_name)
                if event_type in self._handlers:
                    self._handlers[event_type].append(callback)
                else:
                    self._handlers[event_type] = [callback]
        if not added:
            raise ValueError(f'Unknown listener type: {type(listener)}')

    def publish(self, t: T):
        event = ModelEvent(t)
        payload_type = event.generic()
        handlers = self._handlers.get(payload_type)
        if not handlers:
            return
        for handler in handlers:
            handler(event)