from abc import ABC
from typing import List, Dict

from data import MusicState, RepeatOption

class Event(ABC):
    pass

class EventSubscriber:
    def process(self, event: Event):
        pass

class SoundUpdatedEvent(Event):
    def __init__(self, new_volume: int):
        self.new_volume = new_volume

class SpeedUpdatedEvent(Event):
    def __init__(self, new_speed: float):
        self.new_speed = new_speed

class PlaybackChangedEvent(Event):
    def __init__(self, new_state: MusicState):
        self.new_state = new_state

class RepeatOptionChangedEvent(Event):
    def __init__(self, new_repeat: RepeatOption):
        self.new_repeat = new_repeat

class TimeElapsedEvent(Event):
    def __init__(self, elapsed_millis: int):
        self.elapsed_millis = elapsed_millis

class LoadSongsEvent(Event):
    def __init__(self, song_list: List[str]):
        self.song_list = song_list

class SortSongsEvent(Event):
    def __init__(self):
        pass

class ClearSongsEvent(Event):
    def __init__(self):
        pass

class ShuffleSongsEvent(Event):
    def __init__(self):
        pass

class StartSongEvent(Event):
    def __init__(self, song_id: int):
        self.song_id = song_id

class EventRegistry:
    _subscribers: Dict[str, List[EventSubscriber]]

    def register(self, topic: str, event: Event):
        if topic not in self._subscribers:
            return
        subs = self._subscribers[topic]
        for s in subs:
            s.process(event)

    def subscribe(self, topic: str, sub: EventSubscriber):
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        subs = self._subscribers[topic]
        subs.append(sub)

    def __init__(self):
        self._subscribers = {}
